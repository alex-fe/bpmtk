import re


def make_trace(*args):
    """Given a list of node codes, create a trace string.
    Args:
        args (str): List of codes.
    Returns:
        Trace string.
    """
    return '::{}::'.format('::'.join(str(x) for x in args))


def t_split(trace):
    """Split trace  to list of codes.
    Args:
        trace (str): Trace as code chain e.g. ::source::target::
    Returns:
        List of node codes.
    """
    return re.findall('[a-zA-Z0-9]+', trace)
