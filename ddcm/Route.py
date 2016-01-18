import heapq

from .KBucket import KBucket

class Route(object):
    def __init__(self, service, loop, kSize, selfNode):
        self.service = service
        self.loop = loop

        self.selfNode = selfNode
        self.ksize = kSize
        self.buckets = [KBucket(0, 2 ** 160, self.ksize)]

    def getBucket(self, distance):
        for index, bucket in enumerate(self.buckets):
            if bucket.range[0] <= distance < bucket.range[1]:
                return index
                
    def splitBucket(self, index):
        leftBucket, rightBucket = self.buckets[index].split()
        self.buckets[index] = leftBucket
        self.buckets.insert(index + 1, rightBucket)

    def removeNode(self, node):
        __index = self.getBucket(node.distance(self.selfNode))
        self.buckets[__index].removeNode(node)

    def isNewNode(self, node):
        __index = self.getBucket(node.distance(self.selfNode))
        return self.buckets[__index].isNewNode(node)

    def addNode(self, node):
        index = self.getBucket(node.distance(self.selfNode))
        bucket = self.buckets[index]

        if bucket.addNode(node):
            return
        elif bucket.isInRange(node) or bucket.depth() % 5 != 0:
            self.splitBucket(index)
            self.addNode(node)
        else:
            #TODO: Check if the first node is online
            pass

    def findNeighbors(self, node, kSize=None, exclude=None):
        def iter_nodes(bucketIndex):
            def iter_index(startIndex, endIndex, currentIndex):
                __index = currentIndex
                __delta = 0
                yield __index
                while True:
                    __delta += 1
                    if __index + __delta <= endIndex:
                        yield __index + __delta
                    if __index - __delta >= startIndex:
                        yield __index - __delta
                    if __index - __delta <= startIndex and __index + __delta >= endIndex:
                        break
            for index in iter_index(0, len(self.buckets) - 1, bucketIndex):
                for key, value in self.buckets[index].nodes.items():
                    yield value

        kSize = kSize or self.ksize
        nodes = []
        exclude = exclude or []
        __count = 0
        for neighbor in iter_nodes(self.getBucket(node.hash)):
            if neighbor.id != node.id and (not neighbor.id in exclude):
                heapq.heappush(nodes, (neighbor.distance(self.selfNode), neighbor))
                __count += 1
            if len(nodes) is kSize:
                break
        return heapq.nsmallest(__count, nodes)
