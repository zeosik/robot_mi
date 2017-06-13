import os
import threading

import logging

from pathlib import Path
#
#
# class LinkManager:
#
#     def __init__(self):
#         self.logger = logging.getLogger(self.__class__.__name__)
#         self.visited_links = set()
#         self.lock = threading.Lock()
#
#     # ret true if added
#     def add_link(self, link:str):
#         already_exists = link in self.visited_links
#         if not already_exists:
#             try:
#                 self.lock.acquire()
#                 already_exists = link in self.visited_links
#                 if not already_exists:
#                     self.visited_links.add(link)
#                     self.logger.info('adding link: {0}'.format(link))
#             finally:
#                 self.lock.release()
#         return not already_exists
#
#     def is_visited(self, link):
#         result = link in self.visited_links
#         self.logger.debug('result: {0} for link: {1}'.format(result, link))
#         return result
#
