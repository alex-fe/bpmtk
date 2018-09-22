from log.log import LogEdge, LogNode


class DFGEdege(LogEdge):
    """docstring for DFGEdege."""

    def __init__(self, source, target, **kwargs):
        super(DFGEdege, self).__init__(**kwargs)
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
    """docstring for ."""
    def __init__(self, **kwargs):
        super(DFGNode, self).__init__(**kwargs)
