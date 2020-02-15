import urllib.request
from urllib.error import ContentTooShortError


class Download(object):
  """Downloader CTL packages

  Attributes:
    config: configuration values
    url_base: URL path for the file
  """

  def __init__(self, config):
    """Initialize with config values."""
    self.config = config
    self.url_base = self.config['url_base']

  def download(self, filename, local_path):
    """Downloads the package

    Args:
      filename: which file to retrieve
      local_path: absolute path for the file to be downloaded to, including ending '/'

    Returns:
      local_filename: absolute path to the downloaded file

    Raises:
      ContentTooShortError: if the download fails or is incomplete
    """
    url = self.url_base + filename
    local_filename = local_path + filename

    try:
      urllib.request.urlretrieve(url, local_filename)
    except ContentTooShortError as e:
      raise e

    return local_filename