"""Original processMiner.py from client
"""
import datetime
import pygraphviz as pgv
import xml.etree.ElementTree as ET


def run(path):
    tree = ET.parse(path)
    root = tree.getroot()
    log = dict()

    ns = {'xes': 'http://www.xes-standard.org/'}

    for trace in root.findall('xes:trace', ns):
        caseid = ''
        for string in trace.findall('xes:string', ns):
            if string.attrib['key'] == 'concept:name':
                caseid = string.attrib['value']
        for event in trace.findall('xes:event', ns):
            task = ''
            user = ''
            event_type = ''
            for string in event.findall('xes:string', ns):
                if string.attrib['key'] == 'concept:name':
                    task = string.attrib['value']
                if string.attrib['key'] == 'org:resource':
                    user = string.attrib['value']
                if string.attrib['key'] == 'lifecycle:transition':
                    event_type = string.attrib['value']
            timestamp = ''
            for date in event.findall('xes:date', ns):
                if date.attrib['key'] == 'time:timestamp':
                    timestamp = date.attrib['value']
                    timestamp = datetime.datetime.strptime(
                        timestamp[:-10], '%Y-%m-%dT%H:%M:%S'
                    )
            # print(caseid, '|', task, '|', user, '|', timestamp)
            if caseid not in log:
                log[caseid] = []
            event = (task, user, timestamp)
            print(event)
            log[caseid].append(event)


    F = dict()
    for caseid in log:
        for i in range(0, len(log[caseid]) - 1):
            ai = log[caseid][i][0]
            aj = log[caseid][i+1][0]
            if ai not in F:
                F[ai] = dict()
            if aj not in F[ai]:
                F[ai][aj] = 0
            F[ai][aj] += 1

    A = dict()
    for caseid in log:
        for i in range(0, len(log[caseid])):
            ai = log[caseid][i][0]
            if ai not in A:
                A[ai] = 0
            A[ai] += 1

    G = pgv.AGraph(strict=False, directed=True)
    G.graph_attr['rankdir'] = 'LR'
    G.node_attr['shape'] = 'box'

    x_min = min(A.values())
    x_max = max(A.values())
    for ai in A:
        text = ai + '\n' + str(A[ai]) + ')'
        gray = int(float(x_max - A[ai]) / float(x_max - x_min) * 100.00)
        fill = 'gray' + str(gray)
        font = 'black'
        if gray < 50:
            font = 'white'
        G.add_node(ai, label=text, style='filled', fillcolor=fill, fontcolor=font)

    values = [F[ai][aj] for ai in F for aj in F[ai]]
    x_min = min(values)
    x_max = max(values)
    y_min = 1.0
    y_max = 5.0

    for ai in F:
        for aj in F[ai]:
            x = F[ai][aj]
            y = y_min + (y_max - y_min) * float(x - x_min)/float(x_max - x_min)
            G.add_edge(ai, aj, label=x, penwidth=y)

    G.draw('graph.png', prog='dot')
    return log
# processMiner.py
# Displaying processMiner.py.
