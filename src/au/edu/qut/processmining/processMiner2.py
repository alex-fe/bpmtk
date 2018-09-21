import datetime
import os
import pygraphviz as pgv
import xml.etree.ElementTree as ET
from collections import defaultdict


class ProcessMiner(object):

    def __init__(self, xes_file):
        tree = ET.parse(xes_file)
        self.root = tree.getroot()
        self.log = defaultdict(list)
        self.ns = {'xes': 'http://www.xes-standard.org/'}

    def setup(self):
        for trace in self.root.findall('xes:trace', self.ns):
            caseid = ''
            for string in trace.findall('xes:string', self.ns):
                if string.attrib['key'] == 'concept:name':
                    caseid = string.attrib['value']
            for event in trace.findall('xes:event', self.ns):
                task = ''
                user = ''
                # event_type = ''
                for string in event.findall('xes:string', self.ns):
                    if string.attrib['key'] == 'concept:name':
                        task = string.attrib['value']
                    if string.attrib['key'] == 'org:resource':
                        user = string.attrib['value']
                    # Event type is never used.
                    # if string.attrib['key'] == 'lifecycle:transition':
                    #     event_type = string.attrib['value']
                timestamp = ''
                for date in event.findall('xes:date', self.ns):
                    if date.attrib['key'] == 'time:timestamp':
                        timestamp = date.attrib['value']
                        timestamp = datetime.datetime.strptime(
                            timestamp[:-10], '%Y-%m-%dT%H:%M:%S'
                        )
                print(caseid, '|', task, '|', user, '|', timestamp)
                event = (task, user, timestamp)
                self.log[caseid].append(event)
            return task, user

    def set_edge_properties(self):
        """For each case id in log, iterate through number following lists,
        getting ai, and aj (ai+1).Uses a nested collections.defaultdict as to
        add layers if not present.

        Returns:
            Populated nested default dictionary
        """
        F = defaultdict(lambda: defaultdict(int))
        for caseid in self.log:
            for i in range(len(self.log[caseid]) - 1):
                ai = self.log[caseid][i][0]
                aj = self.log[caseid][i+1][0]
                F[ai][aj] += 1
        return F

    def set_node_properties(self):
        """For each case id in log, iterate through length of ids,
        getting ai. If ai present, add 1.

        Returns:
            Populated default dictionary
        """
        A = defaultdict(int)
        for caseid in self.log:
            for i in range(len(self.log[caseid])):
                ai = self.log[caseid][i][0]
                A[ai] += 1
        return A

    def graph(
        self,
        location=os.path.dirname(os.path.realpath(__file__)),
        draw=False
    ):
        """Create graph from XML tree.
        Args:
            location (str): File location; default is the location of
                ProcessMiner2.py
            draw (bool): Draw graph file; default is false.
        Returns:
            Created graph, G.
        """
        G = pgv.AGraph(strict=False, directed=True)
        G.graph_attr['rankdir'] = 'LR'
        G.node_attr['shape'] = 'box'

        A = self.set_node_properties()
        x_min = min(A.values())
        x_max = max(A.values())
        for ai in A:
            text = ai + '\n' + str(A[ai]) + ')'
            gray = int(float(x_max - A[ai]) / float(x_max - x_min) * 100.00)
            fill = 'gray' + str(gray)
            font = 'black'
            if gray < 50:
                font = 'white'
            G.add_node(
                ai, label=text, style='filled', fillcolor=fill, fontcolor=font
            )

        F = self.set_edge_properties()
        values = [F[ai][aj] for ai in F for aj in F[ai]]
        x_min = min(values)
        x_max = max(values)
        y_min = 1.0
        y_max = 5.0

        for ai in F:
            for aj in F[ai]:
                x = F[ai][aj]
                y = (
                    y_min
                    + (y_max - y_min)
                    * float(x - x_min)
                    / float(x_max - x_min)
                )
                G.add_edge(ai, aj, label=x, penwidth=y)
        if draw:
            graph_location = os.path.join(location, 'graph.png')
            G.draw(graph_location, prog='dot')
        return G
