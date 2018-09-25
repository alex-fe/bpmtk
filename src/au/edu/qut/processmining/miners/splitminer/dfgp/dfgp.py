from collections import defaultdict

import utils as u
from log.log import LogEdge, LogNode


class DFGEdge(LogEdge):
    """docstring for DFGEdege."""

    def __init__(self, source, target, **kwargs):
        super(DFGEdge, self).__init__(source, target, **kwargs)
        self.frequency = kwargs.get('frequency', 0)

    def increase_frequency(self, amount=1):
        """Increase the frequency by passed amount.
        Args:
            amount (int): Amount to increase frequency by. Default is 1
        """
        self.frequency += amount

    @property
    def print_(self):
        return '{} > {} [{}]'.format(
            self.source.code, self.target.code, self.frequency
        )

    def __str__(self):
        return str(self.frequency)

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return 'DFGEdge: {} > {}'.format(self.source.code, self.target.code)

    # def __eq__(self, o):
    #     if isinstance(o, DFGEdege):
    #         if self.frequency == o.frequency:
    #             pass
    #         else:
    #
    #     else:
    #         return False


class DFGNode(LogNode):
    pass


class DirectlyFollowGraph(object):

    def __init__(self, log, parallelisms_first=False):
        """
        Args:
            nodes (defaultdict): Node.code: node
        """
        self.log = log
        self.parallelisms_first = parallelisms_first
        self.parallelisms_threshold = 0

        self.dfgp = defaultdict(dict)  # LOOK THIS UP
        self.nodes = defaultdict(dict)
        self.edges = set()
        self.incoming = defaultdict(set)
        self.outgoing = defaultdict(set)

        self.events = log.events
        self.traces = log.traces
        self.start_code = log.start_code
        self.end_code = log.end_code

    # Data management
    def add_node(self, node):
        """Add node to DFG.
        Args:
            node (DFGNode): Node to add to graph.
        """
        self.nodes[node.code] = node

    def remove_node(self, code):
        """Remove node from nodes and edges.
        Args:
            code (int): Code to find exiled node.
        """
        del self.nodes[code]
        removeable = {
            edge for edge in
            self.incoming[code].union(self.outgoing[code])
        }
        for edge in removeable:
            self.remove_edge(edge, False)

    def add_edge(self, edge):
        """Add node to DFG, noting direction.
        Args:
            edge (DFGEdge): Edge to add to graph.
        """
        source = edge.source.code
        target = edge.target.code
        self.edges.add(edge)
        self.incoming[target].add(edge)
        self.outgoing[source].add(edge)
        self.dfgp[source].update({target: edge})

    def remove_edge(self, edge, safe):
        """Remove edge.
        Args:

        Returns:
            Boolean
        """
        source = edge.source.code
        target = edge.target.code
        if (
            safe
            and (
                len(self.incoming[target]) == 1
                or len(self.outgoing[source]) == 1
            )
        ):
            return False
        self.incoming[target].remove(edge)
        self.outgoing[source].remove(edge)
        self.edges.remove(edge)
        del self.dfgp[source][target]
        return True

    def build(self):
        autogen_start = DFGNode(self.events[self.start_code], self.start_code)
        self.add_node(autogen_start)
        autogen_start.increase_frequency(self.log.size)

        autogen_end = DFGNode(self.events[self.end_code], self.end_code)
        self.add_node(autogen_end)
        for t, trace_freq in self.traces.items():
            prev_event = self.start_code
            prev_node = autogen_start
            for trace_code in u.t_split(t):
                event = int(trace_code)  # DEBUG: not sure if correct
                if event not in self.nodes:
                    node = DFGNode(self.events[event], event)
                    self.add_node(node)
                else:
                    node = self.nodes[event]
                node.increase_frequency(trace_freq)
                if (
                    prev_event not in self.dfgp
                    or event not in self.dfgp[prev_event]
                ):
                    edge = DFGEdge(prev_node, node)
                    self.add_edge(edge)
                self.dfgp[prev_event][event].increase_frequency(trace_freq)
                prev_event = event
                prev_node = node

    def detect_loops_simple(self):
        loops = set()
        removable_loop_edges = set()
        for edge in self.edges:
            source = edge.source.code
            target = edge.target.code
            if source == target:
                loops.add(edge)
                removable_loop_edges.add(edge)
        # we removed the loop length 1 edges, because later we will just mark
        # them as self-loop activities
        for edge in removable_loop_edges:
            self.remove_edge(edge, False)
        return loops

    def detect_loops_extended(self, loops):
        loops_extended = set()
        for edge_1 in self.edges:
            source = edge_1.source.code
            target = edge_1.target.code
            if (
                edge_1 not in loops_extended
                and source in self.dfgp[target]
                and source not in loops
                and target not in loops
            ):
                edge_2 = self.dfgp[target][source]
                source_to_target_loop_pattern = u.make_trace(source, target, source)
                source_to_target_loop_freq = 0
                target_to_source_loop_pattern = u.make_trace(target, source, target)
                target_to_source_loop_freq = 0
                for trace, trace_freq in self.traces.items():
                    source_to_target_loop_freq += (
                        source_to_target_loop_pattern.count(trace) * trace_freq
                    )
                    target_to_source_loop_freq += (
                        target_to_source_loop_pattern.count(trace) * trace_freq
                    )
                loop_to_score = (
                    source_to_target_loop_freq + target_to_source_loop_freq
                )
            if loop_to_score:
                loops_extended.add(edge_1, edge_2)
        return loops_extended

    def detect_parallelisns(self, loops, loops_extended):
        parallelisms = defaultdict(set)
        removable_edges = set()
        for edge_1 in self.edges():
            source = edge_1.source.code
            target = edge_1.target.code
            if self.parallelisms_first:
                priority_check = edge_1 not in loops_extended
            else:
                priority_check = (
                    edge_1 not in loops_extended
                    and source not in loops
                    and target not in loops
                )
            if (
                source in self.dfgp[target]
                and priority_check
                and edge_1 not in removable_edges
            ):
                # this means: src || tgt is candidate parallelism
                edge_2 = self.dfpg[target][source]

                source_to_target_freq = edge_1.frequency
                target_to_source_freq = edge_2.frequency
                parallelism_score = float(
                    (source_to_target_freq - target_to_source_freq)
                    / (source_to_target_freq + target_to_source_freq)
                )
                if abs(parallelism_score) < self.parallelisms_threshold:
                    # if parallelismScore is less than the threshold epslon,
                    # we set src || tgt and vice-versa, and we remove edge_1
                    # and edge_2
                    parallelisms[source].add(target)
                    parallelisms[target].add(source)
                    removable_edges.add(edge_1, edge_2)
                else:
                    # or we remove the least frequent edge, edge_1 or edge_2
                    if parallelism_score > 0:
                        removable_edges.add(edge_2)
                    else:
                        removable_edges.add(edge_1)
