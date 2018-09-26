class DiagramHandler(object):
    """docstring for Diagrag."""
    def __init__(self, arg):
        super(DiagramHandler, self).__init__()
        self.arg = arg

    def remove_join_split(diagram):
        """Remove join/split gateways, transforming them into a sequence of a
        join and a split"""
        for join in diagram.gateways():
            pass
