class SplitMiner(object):

    def __init__(self):
        self.bpmn_diagram = None
        self.source = None
        self.sink = None

    def generate_filtered_pdfg(pdfg, n):
        """
        Args:
            pdfg (): Given a DFG G = (N, E), a Pruned DFG (PDFG) is a connected
                graph Gp = (N, Ep), where Ep is the set of edges
                Ep = E \ {(a, b) ∈ E | ab ∨ (¬ab ∧
                (b, a) ∈ E ∧ |a → b| < |b → a|)}
            n (float): Percentile value.
        """
        pass

    def discover_best_incoming_edge(pdfg, i, cf, ei):
        """
        Args:
             pdfg (): Gp = (T, Ep)
             i(): Source
             cf (): Map of forward capacities
             ei (): Map of best incoming edges
        """
        queue = [i]
        unexplored = set()  # this is the set of edges excluding i
        while queue:
            p = queue.pop(0)
            for edge in p:
                # node target of edge
                node = None  # n ← first node in Q;
                capacity_max = min(cf[p], edge.frequency)
                if capacity_max > cf[node]:
                    cf[node] = capacity_max
                    ei[node] = edge
                    if node not in queue:
                        unexplored.add(node)
                if node in unexplored:
                    unexplored.remove(node)
                    queue.append(node)

    def discover_best_outgoing_edge(pdfg, i, cb, eo):
        """
        Args:
             pdfg (): Gp = (T, Ep)
             o (): Sink
             cb (): Map of backward capacities
             eo (): Map of best outgoing edges
        """
        queue = [o]
        unexplored = set()
        while queue:
            n = queue.pop(0)
            for edge in n:
                p = None  # p ← source of e;
                capacity_max = min(cb[p], edge.frequency)
                if capacity_max > cb[p]:
                    cb[p] = capacity_max
                    eo[p] = edge
                    if p not in queue:
                        unexplored.add(p)
                if p in unexplored:
                    unexplored.remove(p)
                    queue.append(p)
"""
Add o to Q;
U ← T \ {o};
while Q = ∅ do
n ← first node in Q;
remove n from Q;
for e ∈ •n do
    p ← source of e;
    fe ← frequency of e;
    Cmax ← Min(Cb[n], fe);
    if Cmax > Cb[p] then
        Cb[p] ← Cmax ;
        Eo[p] ← e;
        if p ∈/ Q ∪ U
            then add p to U;
    if p ∈ U then
        remove p from U;
        add p to Q;
"""
    # def mine_bpmn_diagram(
    #     self, log, x_event_classifier, percentile_frequency_threshold,
    #     parallelisms_threshold, filter_type, parallelisms_first, replace_IORs,
    #     remove_loop_activities, structuring_time
    # ):
    #     """
    #     Args:
    #         log (Xlog)
    #         x_event_classifier (XEventClassifier)
    #         percentile_frequency_threshold (float)
    #         parallelisms_threshold (float)
    #         filter_type (DFGPUIResult.FilterType)
    #         parallelisms_first (bool)
    #         replace_IORs (bool)
    #         remove_loop_activities (bol)
    #         structuring_time (SplitMinerUIResult.StructuringTime/)
    #     """
    #     self.replace_IORs = replace_IORs
    #     self.remove_loop_activities = remove_loop_activities
    #     self.structuring_time = structuring_time
