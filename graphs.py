import os

# @class Graph - TODO
class Graph(object):
    def __init__(self):
        self.nodes = set()
        self.edges = set()
        self.node_degrees = dict()

    @staticmethod
    def mkunique(name):
        return name.replace("/", "_").replace(".", "_")

    def add_node(self, name):
        self.nodes.add(name)
        self.node_degrees[name] = 0.0

    def add_edge(self, node_from, node_to):
        if node_from == node_to:
            return # ignore self edges
        if not node_from in self.nodes:
            self.nodes.add(node_from)
        if not node_to in self.nodes:
            self.nodes.add(node_to)
        self.edges.add((node_from, node_to))
        try:
            self.node_degrees[node_to] += 1.0
        except KeyError:
            self.node_degrees[node_to] = 1.0

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
        node_id = Graph.mkunique(node)
        node_label = os.path.basename(node)
        node_factor = self.node_degrees[node] / len(self.nodes)

        r = 0xff
        g = 0xff - (0xff - 0x55)*node_factor
        b = 0xff - (0xff - 0x55)*node_factor
        node_style = DotGraph.NODE_STYLE.format(DotGraph.mkcolor(r, g, b))
        return "node_{}[label=\"{}\", {}];".format(node_id, node_label, node_style)

    def mkedge(self, node_from, node_to):
        node_from_id = Graph.mkunique(node_from)
        node_to_id = Graph.mkunique(node_to)
        return "node_{} -> node_{};".format(node_from_id, node_to_id)

    def dump(self):
        print "digraph {"

        for node in self.nodes:
            print " ", self.mknode(node)

        for edge in self.edges:
            print " ", self.mkedge(edge[0], edge[1])

        print "}"

# @class Jsonraph - TODO
class JsonGraph(Graph):
    def __init__(self):
        Graph.__init__(self)

    def mknode(self, node):
        node_id = Graph.mkunique(node)
        data_str = "\"id\": \"{}\", \"label\": \"{}\"".format(node_id, node)
        return "{ \"data\": {" + data_str + "} },"

    def mkedge(self, node_from, node_to):
        node_from_id = Graph.mkunique(node_from)
        node_to_id = Graph.mkunique(node_to)
        edge_id = node_from_id + "_" + node_to_id
        data_str = "\"id\": \"{}\", \"source\": \"{}\", \"target\": \"{}\"" \
            .format(edge_id, node_from_id, node_to_id)
        return "{ \"data\": {" + data_str + "} },"

    def dump(self):
        print "{"

        print "  \"nodes\": ["

        for node in self.nodes:
            print "   ", self.mknode(node)

        print "  ],"

        print "  \"edges\": ["

        for edge in self.edges:
            print "   ", self.mkedge(edge[0], edge[1])

        print "  ]"

        print "}"
