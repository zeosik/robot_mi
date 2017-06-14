import logging
import os
import pickle
from pathlib import Path

from statistics import mean
from urllib.parse import urlparse

from networkx import Graph, all_pairs_shortest_path_length, average_clustering, is_connected, DiGraph

from LinkDownloader import LinkDownloader
from LinkExtractor import LinkExtractor


class MyVertex:

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
        self.my_vertexes = []

    def analize(self):
        link_vertex = {}
        while len(self.queue) > 0:# and len(self.hit) < 100 :
            link = self._pop_first()
            html = self._from_cache(link)
            if html is not None:
                self.hit.append(link)
                extractor = LinkExtractor(skip_check_exstentions= True)
                links = set(extractor.get_good_links_from_data(html, self.root))
                not_visited_links = []
                for new_link in links:
                    if new_link not in self.visited:
                        not_visited_links.append(new_link)

                self._add_to_queue(not_visited_links)
                if len(self.hit) % 100 == 0:
                    print('stats {0}/{1} hit:{2}'.format(len(self.visited) - len(self.queue), len(self.visited), len(self.hit)))
                #
                my_vertex = MyVertex(link, links)
                self.my_vertexes.append(my_vertex)
                link_vertex[link] = my_vertex
        self._add_neighbours(link_vertex)

        digraph = DiGraph()
        graph = Graph()
        #my_vertex_g_vertex = {}
        for my_vertex in self.my_vertexes:
            digraph.add_node(my_vertex)
            graph.add_node(my_vertex)
            # g_vertex = g.add_node(my_vertex)
            # my_vertex_g_vertex[my_vertex] = g_vertex

        for source in self.my_vertexes:
            for target in source.neighbours:
                digraph.add_edge(source, target)
                graph.add_edge(source, target)

        #for my_vertex_source, g_vertex_source in my_vertex_g_vertex.items():
        #    for my_vertex_target in my_vertex_source.neighbours:
        #        g_vertex_target = my_vertex_g_vertex[my_vertex_target]
        #        g.add_edge(g_vertex_source, g_vertex_target)

        print ('nodes: {0}'.format(digraph.number_of_nodes()))
        print ('edges: {0}'.format(digraph.number_of_edges()))

        out_d_dict = digraph.out_degree()
        out_d = out_d_dict.values()
        print ('out degree min: {0} max: {1}'.format(min(out_d), max(out_d)))

        in_d_dict = digraph.in_degree()
        in_d = in_d_dict.values()
        print ('in degree min: {0} max: {1}'.format(min(in_d), max(in_d)))


        paths = all_pairs_shortest_path_length(digraph)
        lengths = []
        for s in self.my_vertexes:
            for t in self.my_vertexes:
                if s is not t and s in paths and t in paths[s]:
                    lengths.append(paths[s][t])

        print ('mean: {0}'.format(mean(lengths)))
        print ('diameter: {0}'.format(max(lengths)))

        clustering = average_clustering(graph)

        print ('clustering coefficient : {0}'.format(clustering))


        #odporność na awarie
        disconnected = []
        for my_vertex in self.my_vertexes:
            graph.remove_node(my_vertex)
            if not is_connected(graph):
                disconnected.append(my_vertex)

            #put back
                graph.add_node(my_vertex)
            for neighbour in my_vertex.neighbours:
                graph.add_edge(my_vertex, neighbour)


        print('removing {0}/{1} nodes disconnects graph'.format(len(disconnected), len(self.my_vertexes)))

        self._dump(lengths, 'lengths')
        self._dump(out_d_dict, 'out_d_dict')
        self._dump(in_d_dict, 'in_d_dict')
        self._dump(graph, 'graph')
        self._dump(digraph, 'digraph')
        self._dump(self.my_vertexes, 'my_veertexes')

    def _dump(self, object, name):
        filename = self._file_name(name)
        with open(file=filename, mode='wb') as file:
            pickle.dump(object, file)

    def _file_name(self, name):
        path = Path(os.getcwd()) / 'dump'
        if not path.is_dir():
            path.mkdir()
        filename = str((path / '{0}.txt'.format(name)))
        return filename

    def from_dump(self, name):
        filename = self._file_name(name)
        with open(file=filename, mode='rb') as file:
            return pickle.load(file)

    def _add_neighbours(self, link_vertex):
        for vertex in self.my_vertexes:
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
