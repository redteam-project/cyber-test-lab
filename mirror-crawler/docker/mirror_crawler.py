import os
import urllib.request
from urllib.error import ContentTooShortError

from bs4 import BeautifulSoup

class MirrorCrawler(object):

  def __init__(self):
    self.config = {
      # 'mirror': os.environ.get('MIRROR'),
      'local_path': os.environ.get('LOCAL_PATH')
    }

  def parse(self, url, name) -> list:
    # filename = self.config['local_path'] + '/' + name
    filename = name
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
        self.download(deeper_url, directory + '/' + basename)




def main():
  url = 'http://ftp.osuosl.org/pub/centos/'

  mc = MirrorCrawler()

  mc.download(url, mc.config['local_path'] + '/index.html')
  mc.mirror(url, mc.config['local_path'])


if __name__ == '__main__':
  main()