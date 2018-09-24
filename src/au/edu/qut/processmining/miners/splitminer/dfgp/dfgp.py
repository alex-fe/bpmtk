from collections import defaultdict

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

    def print_(self):
        pass

    def __str__(self):
        return str(self.frequency)

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


class DirectlyFollowGraphPlus(object):

    def __init__(self, log):
        self.log = log
        self.dfgp = defaultdict(dict)  # LOOK THIS UP
        self.nodes = defaultdict(dict)
        self.edges = set()
        self.incoming_edges = defaultdict(set)
        self.outgoing_edges = defaultdict(set)

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
        self.nodes.update({node.code: node})

    def remove_node(self, code):
        """Remove node from nodes and edges.
        Args:
            code (int): Code to find exiled node.
        """
        del self.nodes[code]
        removeable = {
            edge for edge in
            self.incoming_edges[code].union(self.outgoing_edges[code])
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
        self.incoming_edges.get(target).add(edge)
        self.outgoing_edges.get(source).add(edge)
        self.dfgp[source].update(target, edge)

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
                len(self.incoming_edges[target]) == 1
                or len(self.outgoing_edges[source]) == 1
            )
        ):
            return False
        self.incoming_edges[target].remove(edge)
        self.outgoing_edges[source].remove(edge)
        self.edges.remove(edge)
        del self.dfgp[source][target]
        return True

    def build(self):
        autogen_start = DFGNode(self.events[self.start_code], self.start_code)
        self.add_node(autogen_start)
        autogen_start.increase_frequency(len(self.log))

        autogen_end = DFGNode(self.events[self.end_code], self.end_code)
        self.add_node(autogen_end)
        for t, trace_freq in self.traces.items():
            trace = t.split('::')
            prev_event = self.start_code
            prev_node = autogen_start
            while trace:
                event = trace.code  # DEBUG: not sure if correct
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
