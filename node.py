class Node:
    def __init__(self, id, destination=None):
        self.id = id
        self.destination = destination
        self.hash = int.from_bytes(tmpid, byteorder="big")

    def distance(self, node):
        return self.long_id ^ node.long_id
