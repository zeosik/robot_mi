import logging

import LinkChecker
import LinkManager
from LinkDownloader import LinkDownloader
from LinkExtractor import LinkExtractor


class LinkProcessor:

    def __init__(self, link: str, depth: int = 0):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.link = link

        self.depth = depth

    def process(self, max_depth = None):
        if max_depth is not None and self.depth > max_depth:
            self.logger.warning('max depth reached: {0} skipping processing link: {1}'.format(self.depth, self.link))
            return []
        downloader = LinkDownloader(self.link)
        html_data = downloader.load_data()
        links = []
        if html_data is not None:
            extractor = LinkExtractor()
            links = extractor.get_good_links_from_data(html_data, self.link)
        self.logger.info('processing done links_in_page: {0} depth: {1} link: {2}'.format(len(links), self.depth, self.link))
        return links
