class Storage(object):
    """Storage

    An Object storing key-value pairs
    """
    def __init__(self):
        self.data = dict()

    async def store(self, key, value):
        self.data[key] = value

    async def get(self, key):
        return self.data[key]

    async def exist(self, key):
        return key in self.data.keys()
