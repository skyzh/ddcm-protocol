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
