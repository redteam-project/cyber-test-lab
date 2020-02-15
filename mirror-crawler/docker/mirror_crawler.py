import os
import magic
import re
import yaml

from bs4 import BeautifulSoup
from google.cloud import storage


class MirrorCrawler(object):
  def __init__(self):
    self.config = {
      'bucket_name': os.environ.get('BUCKET_NAME'),
      'bucket_path': os.environ.get('BUCKET_PATH'),
      'mirror_files_path': os.environ.get('MIRROR_FILES_PATH'),
      'local_path': os.environ.get('LOCAL_PATH')
    }
    self.storage_client = storage.Client()

  def get_blobs(self) -> list:
    bucket_name = self.config['bucket_name']
    blobs = self.storage_client.list_blobs(bucket_name,
                                           prefix=self.config['mirror_files_path'])
    return blobs

  def get_file(self, path, blob, local_path):
    bucket_name = self.config['bucket_name'] + '/' + path
    bucket = self.storage_client.bucket(bucket_name)
    blob.download_to_filename(local_path + '/' + blob.name.replace('/', '_'))

  def get_type(self, local_path) -> str:
    try:
      file_type = magic.from_file(local_path)
    except Exception as e:
      raise Exception('get_type magic.from_file failed: ' + str(e))

    short_type = 'unknown'
    if 'ASCII' in file_type:
      short_type = 'ascii'
    elif 'HTML' in file_type:
      # if it's ascii or utf-8 html, beautiful soup won't care
      # it's like a honey badger
      short_type = 'html'
    elif 'UTF-8' in file_type:
      short_type = 'utf-8'

    return short_type

  def find_mirrors(self) -> dict:
    mirrors = {}

    path = self.config['mirror_files_path']
    local_path = self.config['local_path']

    blobs = self.get_blobs()
    for blob in blobs:
      self.get_file(path, blob, local_path)
      filename = local_path + '/' + blob.name.replace('/', '_')
      file_type = self.get_type(filename)

      if file_type == 'html':
        with open(filename, 'r') as f:
          soup = BeautifulSoup(f, 'html.parser')
        links = soup.find_all('a')
        for link in links:
          href = link.get('href')
          if href.startswith('http'):
            mirrors[href] = filename
      elif file_type == 'ascii' or file_type == 'utf-8':
        with open(filename, 'r') as f:
          lines = f.readlines()
        for line in lines:
          if line.startswith('#'):
            continue
          if 'http' in line:
            link = re.sub(r'(.*)(https?\S*)(\s*)',
                          r'\2',
                          line)
            mirrors[link] = filename

    return mirrors


def main():
  mc = MirrorCrawler()
  mirrors = mc.find_mirrors()
  pause = True

if __name__ == '__main__':
  main()