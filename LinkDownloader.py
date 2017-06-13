import os
import ssl
import logging
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen


class LinkDownloader:

    def __init__(self, url, cache_location = Path(os.getcwd()) / 'cache_html_only'):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.url = urlparse(url)
        self.data = None
        self.cache_path = Path(cache_location)
        if not self.cache_path.is_dir():
            self.cache_path.mkdir()

    def load_data(self):
        self.data = self._read_from_disc(self.url)
        if self.data is None:
            self.data = self._download(self.url.geturl())
            if self.data is not None:
                self._save_to_disc(self.url, self.data)
        return self.data

    def _download(self, url):
        self.logger.info('downloading url: {0}'.format(url))
        req = Request(url, headers={'User-Agent': 'Mozilla/6.0'})
        res = urlopen(req, context=ssl._create_unverified_context())
        info = res.info()
        data = None
        if info.get_content_type() in ['text/html', 'text/plain']:
            data = res.read()
        else:
            self.logger.info('not a html content: {1} file: {0}'.format(url, info.get_content_type()))
        return data

    def _read_from_disc(self, url):
        data = None
        file = self.url_to_path(url)
        if file.is_file():
            self.logger.info('reading url: {0} from disc: {1}'.format(url.geturl(), file))
            data = file.read_text(encoding='utf-8')
        return data

    def _save_to_disc(self, url, data):
        file = self.url_to_path(url)
        if file.is_file():
            self.logger.warning('already exists file: {0} url: {1}'.format(file.name, url.geturl()))
        else:
            file.write_bytes(data)

    def url_to_path(self, url):
        return Path(self.cache_path) / "_".join([url.scheme, url.netloc, url.path]).replace('.', '_').replace('/', '_')
