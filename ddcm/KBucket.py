from collections import OrderedDict

from . import utils

class KBucket(object):
    def __init__(self, left, right, kSize):
        self.range = (left, right)
        self.nodes = OrderedDict()
        self.replaceNodes = OrderedDict()
        self.ksize = kSize

    def getNodes(self):
        return self.nodes.values()

    def split(self):
        mid = (self.range[0] + self.range[1]) / 2
        leftBucket = KBucket(self.range[0], mid - 1, self.ksize)
        rightBucket = KBucket(mid, self.range[1], self.ksize)
        for node in self.nodes.values():
            thisBucket = leftBucket if node.hash < mid else rightBucket
            thisBucket.nodes[node.id] = node
        return (leftBucket, rightBucket)

    def isInRange(self, node):
        return self.range[0] <= node.hash <= self.range[1]
        
    def isNewNode(self, node):
        return node.id not in self.nodes

    def addNode(self, node):
        if node.id in self.nodes:
            del self.nodes[node.id]
            self.nodes[node.id] = node
        elif len(self.nodes) < self.ksize:
            self.nodes[node.id] = node
        else:
            self.replaceNodes[node.id] = node
            return False
        return True

    def removeNode(self, node):
        if node.id not in self.nodes:
            return
        del self.nodes[node.id]
        if len(self.replacementNodes) > 0:
            __newnode = self.replacementNodes.pop()
            self.nodes[__newnode.id] = __newnode

    def depth(self):
        return len(utils.commonPrefix([n.id for n in self.nodes.values()]))

    def firstNode(self):
        return self.nodes[0]

    def __len__(self):
        return len(self.nodes)
