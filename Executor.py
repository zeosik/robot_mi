from concurrent.futures import FIRST_COMPLETED
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait

import logging

from LinkChecker import LinkChecker
from LinkProcessor import LinkProcessor


class Executor:

    def __init__(self, root_link, max_pages = None, workers=None):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.root = root_link
        self.visited_links = []
        self.not_fetchable_links = []
        self.checker = LinkChecker(self.root)
        self.max_pages = max_pages
        self.future_to_url = {}
        self.workers = workers

    def _process(self, task):
        new_links = task.process()
        return task, new_links

    def _submit_tasks(self, executor, tasks):
        futures = []
        for task in tasks:
            if self.max_pages is None or self.max_pages > len(self.visited_links):
                future = executor.submit(lambda t: self._process(t), task)
                futures.append(future)
                self.future_to_url[future] = task.link
                self.logger.info('spawning new task: {0}'.format(task.link))
        return futures

    def _links_to_tasks(self, links, depth):
        return map(lambda l: LinkProcessor(l, depth), links)

    def _links_to_futures(self, executor, new_links, last_depth):
        links = self._prepare_new_links(new_links)
        self.visited_links += links
        new_tasks = self._links_to_tasks(links, last_depth + 1)
        return self._submit_tasks(executor, new_tasks)

    def work(self):
        tasks = self._links_to_tasks([self.root], 0)
        pages_done = 0

        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            futures = self._submit_tasks(executor, tasks)
            while len(futures) > 0:
                done_future, not_done_futures = wait(futures, return_when=FIRST_COMPLETED)
                new_futures = []
                for done in done_future:
                    pages_done += 1
                    try:
                        completed_task, new_links = done.result()
                    except Exception as exc:
                        self.logger.error('link: {0} generated an exception: {1}'.format(self.future_to_url[done], exc))
                        print('link: {0} generated an exception: {1}'.format(self.future_to_url[done], exc))
                        #futures = not_done_futures # w/e
                    else:
                        self.logger.info('task finished, pages_done: {0} link: {1}'.format(pages_done, completed_task.link) )
                        new_futures += self._links_to_futures(executor, new_links, completed_task.depth)

                futures = list(not_done_futures) + new_futures
                #stats
                in_progress = len(futures)
                calculated = len(self.visited_links) - in_progress
                self.logger.info('stats {0}/{1} waiting: {2}'.format(calculated, len(self.visited_links), in_progress))
                print('stats {0}/{1} waiting: {2}'.format(calculated, len(self.visited_links), in_progress))

    def _prepare_new_links(self, new_links):
        new_unique_links = self._remove_duplicated_links(list(set(new_links)))
        new_fetchable_links = self._remove_not_fetchable_links(new_unique_links)
        return new_fetchable_links

    def _remove_duplicated_links(self, links):
        return filter(lambda link: link not in self.visited_links, links)

    def _remove_not_fetchable_links(self, links):
        ret = []
        for link in links:
            if self.checker.can_fetch(link):
                ret.append(link)
            else:
                self.not_fetchable_links.append(link)
        return ret
        #return map(lambda link: self.checker.can_fetch(link), links)