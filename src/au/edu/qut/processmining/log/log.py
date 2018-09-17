"""
Contains translations of LogParser.java, SimpleLog.java, graph/LogEdge.java,
and graph/LogNode.java
"""
import uuid


class LogEdge(object):

    def __init__(self, **kwargs):
        self.id = str(uuid.uuid4())
        self.source = kwargs.get('source')
        self.target = kwargs.get('target')
        self.label = kwargs.get('label')

    @property
    def source_code(self):
        # TODO: figure out what getCode does
        return self.source.code

    @property
    def target_code(self):
        return self.target.code

    def __eq__(self, o):
        if isinstance(o, LogEdge):
            return self.id == o.id
        else:
            return False


class LogNode(object):

    def __init__(self, **kwargs):
        self.id = kwargs.get('code', str(uuid.uuid4()))
        # TODO: Check if it supposed to be string null or None
        self.frequency = 0
        self.start_frequency = 0
        self.end_frequency = 0
        self.label = kwargs.get('label', "null")
        self.code = kwargs.get('code')

    def increase_frequency(self, amount=1):
        """Increase the frequency by passed amount.
        Args:
            amount (int): Amount to increase frequency by. Default is 1
        """
        self.frequency += amount

    def inc_start_frequency(self, amount=1):
        """Increase the start frequency by passed amount.
        Args:
            amount (int): Amount to increase frequency by. Default is 1
        """
        self.start_frequency += amount

    def inc_end_frequency(self, amount=1):
        """Increase the end frequency by passed amount.
        Args:
            amount (int): Amount to increase frequency by. Default is 1
        """
        self.end_frequency += amount

    @property
    def is_start_event(self):
        """Check if start frequency has changed from original value.
        Returns:
            Boolean self.start_frequency != 0
        """
        return bool(self.start_frequency)

    @property
    def is_end_event(self):
        """Check if end frequency has changed from original value.
        Returns:
            Boolean self.end_frequency != 0
        """
        return bool(self.start_frequency)

    def __eq__(self, o):
        """Check for equality via ids."""
        if isinstance(o, LogNode):
            return self.id == o.id
        else:
            return False


class SimpleLog(object):

    def __init__(self, traces, events, xlog):
        self.events = events
        self.traces = traces
        self.size = sum(trace_freq for trace_freq in traces.values())
        self.xlog = xlog
        self.total_events = -1
        self.longest_trace = -1
        self.shortest_trace = -1

    @property
    def distintic_traces(self):
        return len(self.traces)

    @property
    def distintic_events(self):
        return len(self.traces) - 2

    @property
    def avg_trace_length(self):
        return self.total_events / self.size


class LogParser(object):
    """docstring for LogParser."""
    def __init__(self, arg):
        super(LogParser, self).__init__()
        self.arg = arg
