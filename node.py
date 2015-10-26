class Node:
    def __init__(self, id, remote=None):
        """Node

        Args:
            id: Node id, a bytes object
        """
        self.id = id
        self.remote = remote
        self.hash = int.from_bytes(id, byteorder="big")

    def distance(self, node):
        return self.hash ^ node.hash
