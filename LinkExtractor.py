import logging
from urllib.parse import urlparse, urljoin, urldefrag

from bs4 import BeautifulSoup
from bs4 import SoupStrainer


class LinkExtractor:

    def __init__(self, skip_check_exstentions = False):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.skip_check_exstentions = skip_check_exstentions

    def get_good_links_from_data(self, html_data, root):
        links = self._find_links(html_data)
        links = self._same_domain_links(root, links)
        links = self._unfragmented_urls(links)
        links = self._skip_weird_exstension_files(links)
        #links = self._fetchable_urls(links, checker)
        return links

    def _find_links(self, data):
        links = []
        for link in BeautifulSoup(data, parse_only=SoupStrainer('a'), from_encoding='utf8'):
            if link.has_attr('href'):
                links.append(link['href'])
        return links

    def _same_domain_links(self, root, links):
        ret = []
        root_url = urlparse(root)
        for link in links:
            url = urlparse(urljoin(root, link))
            if root_url.netloc == url.netloc: # or url.netloc.endswith('cam.ac.uk'):
                ret.append(url.geturl())
            else:
                self.logger.debug('link form different domain: {0}'.format(url.geturl()))
        return ret

    def _unfragmented_urls(self, links):
        ret = []
        for link in links:
            ret.append(urldefrag(link).url)
        return ret

    def _fetchable_urls(self, links, checker):
        ret = []
        for link in links:
            if checker.can_fetch(link):
                ret.append(link)
        return ret

    def _skip_weird_exstension_files(self, links):
        if (self.skip_check_exstentions):
            return links
        ret = []
        extensions = ['.tar.bz2', '.zip', '.exe', '.pdf', '.gz', '.dmg', '.asc', '.msi', '.pkg', '.tgz', '.doc', 'docx']
        for link in links:
            if link.endswith(tuple(extensions)):
                self.logger.debug('skipping link: {0}'.format(link))
            else:
                ret.append(link)
        return ret