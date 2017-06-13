from urllib.parse import urlparse

import logging
from reppy.robots import Robots


class LinkChecker:

    def __init__(self, domain):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.domain_url = urlparse(domain)
        self.robots_url = urlparse(Robots.robots_url(domain))
        self.robots = Robots.fetch(self.robots_url.geturl())
        self.agent = self.robots.agent('*')

    def can_fetch(self, url):
        can_fetch = self.agent.allowed(url)
        self.logger.debug('result: {0} for link: {1}'.format(can_fetch, url))
        return can_fetch
