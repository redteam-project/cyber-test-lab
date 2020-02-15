import os
import magic

from google.cloud import bigquery
from google.cloud import storage


class MirrorCrawler(object):
  def __init__(self):
    self.config = {
      'bucket_name': os.environ.get('BUCKET_NAME'),
      'bucket_path': os.environ.get('BUCKET_PATH'),
      'mirror_files_path': os.environ.get('MIRROR_FILES_PATH')
    }
    self.storage_client = storage.Client()

  def get_blobs(self, path) -> list:
    bucket_name = self.config['bucket_name'] + '/' + self.config[path]
    blobs = self.storage_client.list_blobs(bucket_name)
    return blobs

  def get_file(self, path, filename, local_path):
    bucket_name = self.config['bucket_name'] + '/' + self.config[path]
    bucket = self.storage_client.bucket(bucket_name)
    blob = bucket.blob(filename)
    blob.download_to_filename(local_path)

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



def main():
  pass

if __name__ == '__main__':
  main()