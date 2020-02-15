import os

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

def main():
  pass

if __name__ == '__main__':
  main()