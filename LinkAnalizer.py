import logging

from pathlib import Path
from urllib.parse import urlparse

from LinkDownloader import LinkDownloader
from LinkExtractor import LinkExtractor


class Vertex:

    def __init__(self, name, links):
        self.name = name
        self.all_links = links
        self.neighbours = []


class LinkAnalizer:

    def __init__(self, root):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.root = root
        self.queue = [root]
        self.visited = set()
        self.hit = []
        self.v = []

    def analize(self):
        link_vertex = {}
        while len(self.queue) > 0:
            link = self._pop_first()
            html = self._from_cache(link)
            if html is not None:
                self.hit.append(link)
                extractor = LinkExtractor(skip_check_exstentions= True)
                links = set(extractor.get_good_links_from_data(html, self.root))
                not_visited_links = filter(lambda l: l not in self.visited, links)
                self._add_to_queue(not_visited_links)
                if len(self.hit) % 100 == 0:
                    print('stats {0}/{1} hit:{2}'.format(len(self.visited) - len(self.queue), len(self.visited), len(self.hit)))
                #
                vertex = Vertex(link, links)
                self.v.append(vertex)
                link_vertex[link] = vertex
        self._add_neighbours(link_vertex)

        maxd = 0
        maxv = None
        for vv in self.v:
            local = len(vv.neighbours)
            if local > maxd:
                maxd = local
                maxv = vv

        print("maxd: {0} for link: {1}".format(maxd, maxv.name))

    def _add_neighbours(self, link_vertex):
        for vertex in self.v:
            for link in vertex.all_links:
                if link in link_vertex:
                    vertex.neighbours.append(link_vertex[link])

    def _pop_first(self):
        link = self.queue[0]
        self.queue = self.queue[1:]
        return link

    def _add_to_queue(self, links):
        for link in links:
            if link in self.visited:
                self.logger.warning('link already marked as visited: {0}'.format(link))
            self.visited.add(link)
            self.queue.append(link)

    def _from_cache(self, link):
        try:
            reader = LinkDownloader(link)
            html = reader._read_from_disc(urlparse(link))
            return html
        except Exception as exc:
            pass
        return None
