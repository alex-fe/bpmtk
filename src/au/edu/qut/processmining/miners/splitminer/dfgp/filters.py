import sys
from collections import deque


class Filter(object):

    best_edges = set()
    filter_threshold = None
    to_visit = deque()

    @classmethod
    def _best_edges_on_max_freq(cls, graph):
        for node in graph.nodes.keys():
            if node != graph.end_code and node in graph.outgoing:
                cls.best_edges.add(max(graph.outgoing[node]))
            if node != graph.start_code and node in graph.incoming:
                cls.best_edges.add(max(graph.incoming[node]))

    @classmethod
    def _compute_filter_threshold(cls, percentile_frequency_threshold):
        """
        Args:
            percentile_frequency_threshold
        """
        i = round(len(cls.best_edges) * percentile_frequency_threshold)
        i -= 1 * (i == len(cls.best_edges))
        cls.filter_threshold = cls.best_edges[i].frequency

    @classmethod
    def _reapply_edges(cls, graph, edges, use_threshold=False):
        for edge in edges:
            if use_threshold and edge.frequency == cls.filter_threshold:
                graph.add_edge(edge)
            else:
                source = edge.source.code
                target = edge.target.code
                if not graph.outgoing[source] or not graph.incoming[target]:
                    graph.add_edge(edge)

    @staticmethod
    def _directionals(graph, forward):
        if forward:
            return graph.start_code, graph.end_code, graph.outgoing, 'source'
        else:
            return graph.end_code, graph.start_code, graph.incoming, 'target'

    @classmethod
    def _traverse(cls, graph, forward, use_capacity):
        start, end, direction, directional = cls._directionals(graph, forward)
        node_set = set(graph.nodes.keys())
        max_capacity = {node: 0 for node in node_set}
        max_capacity[start] = sys.maxsize
        cls.to_visit.append(start)
        unvisited = node_set
        unvisited.remove(start)
        best = {}
        while cls.to_visit:
            n1 = cls.to_visit.popleft()
            cap = cls.max_cap[n1]
            for edge in direction[n1]:
                n2 = getattr(edge, directional).code
                if use_capacity:
                    max_cap = edge.frequency if cap > edge.frequency else cap
                    if max_cap > max_capacity[n2]:
                        max_capacity[n2] = max_cap
                        best[n2] = edge
                        if n2 not in cls.to_visit:
                            unvisited.add(n2)
                if n2 in unvisited:
                    cls.to_visit.append(n2)
                    unvisited.remove(n2)
        return best

    @classmethod
    def standard(cls, graph):
        cls._best_edges_on_max_freq(graph)
        for edge in graph.edges:
            graph.remove_edge(edge)
        frequency_ordered_edges = sorted(cls.best_edges, reverse=True)
        cls._reapply_edges(graph, frequency_ordered_edges)

    @classmethod
    def with_threshold(cls, graph, percentile_frequency_threshold):
        cls._best_edges_on_max_freq(graph)
        cls._compute_filter_threshold(percentile_frequency_threshold)

        ordered_most_frequent_edges = cls.best_edges.copy()
        for edge in ordered_most_frequent_edges:
            graph.remove_edge(edge, False)
        for edge in graph.edges:
            if edge.frequency > cls.filter_threshold:
                ordered_most_frequent_edges.add(edge)
            graph.remove_edge(edge, False)
        cls._reapply_edges(graph, ordered_most_frequent_edges, True)

    @classmethod
    def with_guarantees(cls, graph, percentile_frequency_threshold):
        cls._best_edges_on_max_freq(graph)
        cls._compute_filter_threshold(percentile_frequency_threshold)
        best_predecessor = cls._traverse(graph, True, True)
        best_successor = cls._traverse(graph, False, True)

        for node in graph.nodes.keys():
            cls.best_edges.add(best_predecessor[node])
            cls.best_edges.add(best_successor[node])
        # cls.best_edges.remove(None)
        for edge in graph.edges:
            if (
                edge not in cls.best_edges and
                edge.frequency >= cls.filter_threshold
            ):
                graph.remove_edge(edge, False)

    @classmethod
    def explore_and_remove(cls, graph):
        cls._traverse(graph, True, False)
        cls._traverse(graph, False, False)
