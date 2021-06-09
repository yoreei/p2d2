from collections import deque


class Traverser:
    def __init__(self, *nodetypes: str):
        self.result = deque([])
        for nodetype in nodetypes:
            self.__dict__["visit_" + nodetype] = self.enqueue

    def enqueue(self, node):
        self.result.append(node)
        return self.recurse(node)

    def print_node(self, node):
        print(node)

    def recurse(self, node):
        for child in node.get_children():
            print(child)
            child.accept(self)

    def __getattr__(self, attr):
        if attr in self.__dict__:
            return self.attr
        else:
            # print('dunno')
            return self.recurse
