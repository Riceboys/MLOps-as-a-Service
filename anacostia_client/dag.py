
class DAG(object):
    def __init__(self):
        self.nodes = []

    def add_node(self, node):
        self.nodes.append(node)
    
    def add_edge(self, parent, child):
        parent.add_child(child)

    def run(self):
        for node in self.nodes:
            node.run()

class Node(object):
    def __init__(self, name, **kwargs):
        self.name = name
        self.children = []

    def run(self):
        raise NotImplementedError
