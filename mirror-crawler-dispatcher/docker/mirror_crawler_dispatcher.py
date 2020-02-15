import os
import magic
import re
import yaml

from bs4 import BeautifulSoup
from google.cloud import storage


class MirrorCrawlerDispatcher(object):
  """cyber-test-lab mirror-crawler dispatcher"""

  def __init__(self):
    """init function for the dispatcher.

       This object is intended to be called by a Kubernetes batch job. It
       assumes the following environment varibles are set:
         GOOGLE_APPLICATION_CREDENTAILS: creds json file for access to GCP APIs
         BUCKET_NAME: the root GCS bucket in which mirror-monitor files can be
                      found
         MIRROR_FILES_PATH: the sub-directory in which the distros' mirror
                            files can be found
         LOCAL_PATH: local directory in which the distros' mirror files will
                     be stored for processing with this class
    """

    # set config data from environment variables
    # note: no need to set GOOGLE_APPLICAION_CREDENTIALS as the google.cloud
    #       look those up on their own
    self.config = {
      'bucket_name': os.environ.get('BUCKET_NAME'),
      'mirror_files_path': os.environ.get('MIRROR_FILES_PATH'),
      'local_path': os.environ.get('LOCAL_PATH')
    }

    # load config data from container's yaml config file
    with open('config.yaml', 'r') as f:
      yc = yaml.safe_load(f)

    # doing a manual merge of these values because it's easier to read
    self.config['architectures'] = yc['architectures']
    self.config['blacklist'] = yc['blacklist']
    self.config['distros'] = yc['distros']

    # creating the GCS client here for easy reuse
    self.storage_client = storage.Client()

  def get_blobs(self) -> list:
    """Recursively get the blobs in GCS

    Returns:
      blobs: a list of all blobs in GCS
    """
    bucket_name = self.config['bucket_name']
    blobs = self.storage_client.list_blobs(bucket_name,
                                           prefix=self.config[
                                             'mirror_files_path'])
    return blobs

  def get_file(self, path, blob, local_path):
    """Downloads an individual file from GCS

    Args:
      path: the bucket's path
      blob: the GCS blob
      local_path: location to cache this blob
    """
    bucket_name = self.config['bucket_name'] + '/' + path
    bucket = self.storage_client.bucket(bucket_name)
    blob.download_to_filename(local_path + '/' + blob.name.replace('/', '_'))

  def get_type(self, local_path) -> str:
    """Determine's a file's type using python-magic

    Args:
      local_path: the local object who's type we want to know

    Returns:
      file_type: python-magic's file type

    Raises:
      Exception: if magic.from_file raises an exception
    """
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

  def find_mirrors(self) -> list:
    """Finds mirror urls in the mirror-monitor files

    Returns:
      filtered_mirrors: a deduplicated list of mirror urls
    """
    mirrors = {}

    path = self.config['mirror_files_path']
    local_path = self.config['local_path']

    blobs = self.get_blobs()
    for blob in blobs:
      self.get_file(path, blob, local_path)

      # the blobs' paths will contain lots of slash characters, so we'll
      # replace them with underscores
      filename = local_path + '/' + blob.name.replace('/', '_')

      file_type = self.get_type(filename)

      if file_type == 'html':
        # if the file_type is html, let BeautifulSoup find all the links
        with open(filename, 'r') as f:
          soup = BeautifulSoup(f, 'html.parser')
        links = soup.find_all('a')
        for link in links:
          href = link.get('href')
          if href.startswith('http'):
            mirrors[href] = filename

      elif file_type == 'ascii' or file_type == 'utf-8':
        # if the file is ascii or utf-8 we need to find the links with regexp

        with open(filename, 'r') as f:
          lines = f.readlines()
        for line in lines:
          if line.startswith('#'):
            # discard comment lines
            continue

          if 'http' in line:
            # pull out the link pattern
            link = re.sub(r'(.*)(https?\S*)(\s*)',
                          r'\2',
                          line)

            # some lines end up with "s in them, so discard that and any
            # following characters
            link = re.sub(r'".*', r'', link)

            # get rid of any residual newlines
            link = re.sub(r'\n*', r'', link)

            # now we store the link as a dict key for dedupe purposes
            mirrors[link] = filename

    m = {}
    for link in mirrors.keys():

      # there are some patterns of urls we don't want to mirror, so discard
      # any urls that contain our blacklist strings
      blacklisted = False
      blacklist = self.config['blacklist']
      for b in blacklist:
        if b in link:
          blacklisted = True

      if not blacklisted:
        # some distros have variable patterns that need to be substituted,
        # if that's the case we need to generate permutations based on those
        # variables

        distros = self.config['distros']
        for distro in distros.keys():
          if distros[distro] is None:
            # no permutations, just store the link and continue
            # we shouldn't have a distro name missing from the config yaml, but
            # just in case we'll do this
            m[link] = 1
            continue

          permutations = self.config['distros'][distro].get('permutations', [])
          if len(permutations) == 0:
            # no permutations, just store the link and continue
            m[link] = 1
            continue

          if distro in link:
            for permutation in permutations:

              # retrieve permutations and variables substitutions
              patterns = permutation.keys()

              # iterate over our variables
              for pattern in patterns:
                link = link.replace('$' + pattern, str(permutation[pattern]))

              # no variables, just store the link and continue
              if '$' not in link:
                m[link] = 1

    # one last step is to dedupe any duplicate urls we've generated by accident
    filtered_mirrors = list(m.keys())

    return filtered_mirrors


def main():
  mcd = MirrorCrawlerDispatcher()
  mirrors = mcd.find_mirrors()
  pause = True


if __name__ == '__main__':
  main()
