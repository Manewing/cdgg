import os
import re


class Node(object):
    def __init__(self, path, group):
        self.path = path
        self.name = os.path.basename(self.path)
        self.degree = 1.0
        self.group = group
        self.id = re.sub("[/.]", "_", self.path)
        self.edges = set()

    def addEdge(self, edge):
        self.edges.add(edge)


# @class Graph - TODO
class Graph(object):
    def __init__(self):
        self.nodes = dict()
        self.edges = set()

    def addNode(self, path, group):
        self.nodes[path] = Node(path, group)

    def addEdge(self, path_from, path_to):
        if path_from == path_to:
            return # ignore self edges

        try:
            node_from = self.nodes[path_from]
            node_to = self.nodes[path_to]
            edge = (node_from, node_to)
            node_from.addEdge(edge)
            node_to.addEdge(edge)
            self.edges.add(edge)
        except KeyError as e:
            raise KeyError("no such node: " + str(e))

    def dump(self):
        raise RuntimeError("error abstract method called: Graph.dump")

# @class DotGraph - TODO
class DotGraph(Graph):
    NODE_STYLE = "shape=rectangle, style=filled, fillcolor=\"{}\""

    def __init__(self):
        Graph.__init__(self)

    @staticmethod
    def mkcolor(r, g, b):
        return "#" + hex(int(r))[2:] + hex(int(g))[2:] + hex(int(b))[2:]

    def mknode(self, node):
        nd_factor = node.degree / len(self.nodes)

        r = 0xff
        g = 0xff - (0xff - 0x55)*nd_factor
        b = 0xff - (0xff - 0x55)*nd_factor
        nd_style = DotGraph.NODE_STYLE.format(DotGraph.mkcolor(r, g, b))
        return "node_{}[group=\"{}\", label=\"{}\", {}];".format(node.id,
                node.group, node.name, nd_style)

    def mkedge(self, node_from, node_to):
        return "node_{} -> node_{};".format(node_from.id, node_to.id)

    def dump(self):
        print "digraph {"

        clusters = dict()
        for node in self.nodes.itervalues():
            try:
                clusters[node.group].add(node)
            except KeyError:
                clusters[node.group] = set([node])

        for key, cluster in clusters.items():
            print "  subgraph cluster_"+str(key)+" {"

            for node in cluster:
                print "   ", self.mknode(node)
            print "  }"

        for edge in self.edges:
            print " ", self.mkedge(edge[0], edge[1])

        print "}"

# @class Jsonraph - TODO
class JsonGraph(Graph):
    def __init__(self):
        Graph.__init__(self)

    def mknode(self, node):
        data_str = "\"id\": \"{}\", \"label\": \"{}\"".format(node.id, node.name)
        return "{ \"data\": {" + data_str + "} },"

    def mkedge(self, node_from, node_to):
        edge_id = node_from.id + "_" + node_to.id
        data_str = "\"id\": \"{}\", \"source\": \"{}\", \"target\": \"{}\"" \
            .format(edge_id, node_from.id, node_to.id)
        return "{ \"data\": {" + data_str + "} },"

    def dump(self):
        print "{"

        print "  \"nodes\": ["

        for node in self.nodes.itervalues():
            print "   ", self.mknode(node)

        print "  ],"

        print "  \"edges\": ["

        for edge in self.edges:
            print "   ", self.mkedge(edge[0], edge[1])

        print "  ]"

        print "}"
