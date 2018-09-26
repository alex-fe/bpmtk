import sys

# from dfgp.dfgp import DirectlyFollowGraph


class SplitMiner(object):
    """Starting from a log, Split Miner produces a BPMN model in six steps:
    1) Construct a Directly Follows Graph (DFG).
    2) Analyze for short-loops and self-loops. "In a DFG, a concurrency
        relation between two tasks, e.g. a and b, shows up as two arcs: one
        from a to b and another from b to a, meaning that causality and
        concurrency are mixed up. To address this issue, whenever a likely
        concurrency relation between a and b is discovered, the arcs between
        these two tasks are pruned from the DFG" i.e. a PDFG.
    3) Apply aglo. "A filtering algorithm is applied on the PDFG to strike
        balanced fitness and precision maintaining low control-flow complexity"
    4) "Split gateways are discovered for each task in the filtered PDFG with
        more than one outgoing arc."
    5) "Join gateways are discovered from tasks with multiple incoming arcs"
    6) Find OR-joins and remove where possible.
    """

    def __init__(self, event_log):
        self.log = event_log

    def trasform(self):
        gate_counter = -sys.maxsize
        # we retrieve the starting BPMN diagram from the DFGP, it is a DFGP
        # with start and end events, but no gateways
        bpmn_diagram = self.dfgp.convert_to_BPMNDiagram()
        # firstly we generate the split gateways. There are only two events in
        # the initial BPMN diagram, one is the START and for exclusion the
        # second is the END


    # def build_directly_follow_graph(self):
    #     self.dfg = DirectlyFollowGraph(self.log)
    #     self.dfg.build()
    #
    # def detect_loops():
    #     pass
    #
    # def generate_filtered_pdfg(pdfg, n, source, sink):
    #     """
    #     Args:
    #         pdfg (): Given a DFG G = (N, E), a Pruned DFG (PDFG) is a connected
    #             graph Gp = (N, Ep), where Ep is the set of edges
    #             Ep = E \ {(a, b) ∈ E | ab ∨ (¬ab ∧
    #             (b, a) ∈ E ∧ |a → b| < |b → a|)}
    #         n (float): Percentile value.
    #     """
    #     for edge in pdfg:
    #         pass
    #
    # def discover_best_edge(pdfg, original_node, capacities, edges):
    #     """
    #     Args:
    #          pdfg (): Gp = (T, Ep)
    #          original_node(): Source/sink
    #          capacities (): Map of forward capacities
    #          edges (): Map of best incoming edges
    #     """
    #     queue = [original_node]
    #     unexplored = set()  # this is the set of edges excluding i
    #     while queue:
    #         p = queue.pop(0)
    #         for edge in p:
    #             # node target of edge
    #             node = None  # n ← first node in Q;
    #             capacity_max = min(capacities[p], edge.frequency)
    #             if capacity_max > capacities[node]:
    #                 capacities[node] = capacity_max
    #                 edges[node] = edge
    #                 if node not in unexplored.union(set(queue)):
    #                     unexplored.add(node)
    #             if node in unexplored:
    #                 unexplored.remove(node)
    #                 queue.append(node)
