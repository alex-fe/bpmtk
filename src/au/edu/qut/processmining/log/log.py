"""
Contains translations of LogParser.java, SimpleLog.java, graph/LogEdge.java,
and graph/LogNode.java
"""
import uuid


class LogEdge(object):

    def __init__(self, source, target, **kwargs):
        self.id = str(uuid.uuid4())
        self.source = source
        self.target = target
        self.label = kwargs.get('label')

    def __eq__(self, o):
        if isinstance(o, LogEdge):
            return self.id == o.id
        else:
            return False


class LogNode(object):

    def __init__(self, label=None, code=None):
        self.id = str(uuid.uuid4()) if code is None else str(code)
        # TODO: Check if it supposed to be string null or None
        self.frequency = 0
        self.start_frequency = 0
        self.end_frequency = 0
        self.label = label
        self.code = code

    def increase_frequency(self, amount=1):
        """Increase the frequency by passed amount.
        Args:
            amount (int): Amount to increase frequency by. Default is 1
        """
        self.frequency += amount

    def inc_start_frequency(self):
        """Increase the start frequency by 1."""
        self.start_frequency += 1

    def inc_end_frequency(self):
        """Increase the end frequency by 1."""
        self.end_frequency += 1

    @property
    def is_start_event(self):
        """Check if start frequency has changed from original value.
        Returns:
            Boolean self.start_frequency != 0
        """
        return not bool(self.start_frequency)

    @property
    def is_end_event(self):
        """Check if end frequency has changed from original value.
        Returns:
            Boolean self.end_frequency != 0
        """
        return not bool(self.end_frequency)

    def __eq__(self, o):
        """Check for equality via ids."""
        if isinstance(o, LogNode):
            return self.id == o.id
        else:
            return False


class SimpleLog(object):

    def __init__(self, traces, events, xlog):
        """
        Args:
            traces (dict): Each trace is a string associated to its frequency
            events (dict) Code of the event to its original name; int: str
        """
        self.events = events
        self.traces = traces
        self.size = sum(traces.values())
        self.xlog = xlog
        self.total_events = -1
        self.longest_trace = -1
        self.shortest_trace = -1

    @property
    def distintic_traces(self):
        return len(self.traces)

    @property
    def distintic_events(self):
        return len(self.events) - 2

    @property
    def avg_trace_length(self):
        return self.total_events / self.size
