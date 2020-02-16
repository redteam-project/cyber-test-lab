import os
import urllib.request
from urllib.error import ContentTooShortError
import hashlib
import datetime

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
    try:
      urllib.request.urlretrieve(url, filename)
    except ContentTooShortError as e:
      raise e

  def mirror(self, url, directory):
    index_path = directory + '/index.html'

    links = self.parse(url, index_path)
    for link in links:
      deeper_url = url + '/' + link

      if link.endswith('/'):
        basename = link.split('/')[-2]
        try:
          os.mkdir(directory + '/' + basename)
        except FileExistsError as e:
          pass
        deeper_directory = directory + '/' + basename
        self.download(deeper_url, deeper_directory + '/index.html')
        self.mirror(deeper_url, deeper_directory)
      else:
        basename = link.split('/')[-1]
        path = directory + '/' + basename
        self.download(deeper_url, path)
        self.process_file(deeper_url, path)

  def process_file(self, url, path):
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

    if results.num_results == 0:
      pause = True
      now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
      rows_to_insert = [(filename, sha256, url, now)]
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
  mc.download(url, mc.config['local_path'] + '/index.html')
  mc.mirror(url, mc.config['local_path'])


if __name__ == '__main__':
  main()