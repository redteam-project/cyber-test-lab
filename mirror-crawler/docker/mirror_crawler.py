import os
import urllib.request
from urllib.error import ContentTooShortError, HTTPError
from socket import socket
import ssl
import hashlib
import datetime
import OpenSSL

from bs4 import BeautifulSoup
from google.cloud import bigquery
from google.cloud import storage

class MirrorCrawler(object):

  def __init__(self):
    self.config = {
      'mirror': os.environ.get('MIRROR'),
      'project': os.environ.get('PROJECT'),
      'bq_dataset': os.environ.get('BQ_DATASET'),
      'bq_table': os.environ.get('BQ_TABLE'),
      'bucket_name': os.environ.get('BUCKET_NAME'),
      'bucket_path': os.environ.get('BUCKET_PATH'),
      'local_path': os.environ.get('LOCAL_PATH')
    }
    self.storage_client = storage.Client()
    self.bq_client = bigquery.Client()

  def parse(self, url, filename) -> list:
    with open(filename, 'r') as f:
      soup = BeautifulSoup(f, 'html.parser')
    links = soup.find_all('a')

    filtered_links = {}
    for link in links:
      href = link.get('href')
      if (href.startswith(url) or not href.startswith('http')) and not \
          (href.startswith('?') or href.startswith('/')):
        filtered_links[href] = 1
    try:
      os.unlink(filename)
    except FileNotFoundError as e:
      raise Exception('could not delete: ' + str(e))

    return list(filtered_links.keys())

  def download(self, url, filename):

    server_cert = None
    cert_valid = None

    # capture server cert
    if url.startswith('https'):
      hostname = url.split('/')[2]
      cert = ssl.get_server_certificate((hostname, 443))
      x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
      server_cert = OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM,
                                                    x509)

    try:
      cert_valid = True
      # req = urllib.request.Request(
      #     url,
      #     data=None,
      #     headers={
      #         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'
      #     }
      # )
      # urllib.request.urlretrieve(url, filename)
      response = urllib.request.urlopen(url)
      data = response.read()
      with open(filename, 'wb') as f:
        f.write(data)
    except ssl.SSLError as e:
      try:
        cert_valid = False
        context = ssl._create_unverified_context()
        response = urllib.request.urlopen(url, context=context)
        data = response.read()
        with open(filename, 'wb') as f:
          f.write(data)
      except Exception as e:
        raise e
    except urllib.error.URLError as e:
      raise e
    except Exception as e:
      # todo: be more precise with exception handling
      raise e

    return server_cert, cert_valid

  def mirror(self, url, cert, directory):
    index_path = directory + '/index.html'

    links = self.parse(url, index_path)
    for link in links:

      # avoid previous directory links
      if '/../' in link:
        continue
      deeper_url = url + '/' + link

      if link.endswith('/'):
        basename = link.split('/')[-2]
        try:
          os.mkdir(directory + '/' + basename)
        except FileExistsError as e:
          pass
        deeper_directory = directory + '/' + basename
        self.download(deeper_url, deeper_directory + '/index.html')
        self.mirror(deeper_url, cert, deeper_directory)
      else:
        basename = link.split('/')[-1]
        path = directory + '/' + basename
        self.download(deeper_url, path)
        self.process_file(deeper_url, cert, path)

  def process_file(self, url, cert, path):
    filename = os.path.basename(path)
    with open(path, 'rb') as f:
      file_bytes = f.read()
    sha256 = hashlib.sha256(file_bytes).hexdigest()

    query = "SELECT " \
            "  filename AS filename, " \
            "  sha256 AS sha256, " \
            "FROM {}.{} " \
            "WHERE filename = '{}' AND sha256 = '{}'".format(self.config['bq_dataset'],
                                                             self.config['bq_table'],
                                                             filename,
                                                             sha256)
    query_job = self.bq_client.query(query)
    results = query_job.result()

    if len(list(results)) == 0:
      now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
      server_cert = u''
      if cert[0]:
        server_cert = cert[0].decode('utf-8')
      else:
        server_cert = None
      rows_to_insert = [(filename, sha256, url, now, server_cert, cert[1])]
      table_id = self.config['project'] + '.' + \
                 self.config['bq_dataset'] + '.' + \
                 self.config['bq_table']
      table = self.bq_client.get_table(table_id)
      errors = self.bq_client.insert_rows(table, rows_to_insert)
      if errors:
        raise Exception('bq insert failed on ' + str(rows_to_insert))
      else:
        print('[+] inserted ' + str(rows_to_insert))

      bucket_name = self.config['bucket_name']
      bucket = self.storage_client.get_bucket(bucket_name)
      url_path = url.replace('http://', '').replace('https://', '').replace('//', '/')
      blob = bucket.blob(self.config['bucket_path'] + url_path + '/' + filename)
      blob.upload_from_filename(path)
      print('[+] uploaded ' + path + ' to GCS')

      try:
        os.unlink(path)
      except IOError as e:
        raise Exception('failed to delete ' + path + ': ' + str(e))


def main():
  url = os.environ.get('MIRROR')

  mc = MirrorCrawler()
  server_cert = mc.download(url, mc.config['local_path'] + '/index.html')
  mc.mirror(url, server_cert, mc.config['local_path'])


if __name__ == '__main__':
  main()