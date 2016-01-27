import random
import json
import codecs
import itertools

import os.path

def commonPrefix(data):
    def bits(item):
        def _bits(n):
            return reversed([0 if (n & (1 << i)) is 0 else 1 for i in range(8)])
        return list(itertools.chain(*[list(_bits(n)) for n in item]))
    return os.path.commonprefix([bits(item) for item in data])

def get_echo_bytes():
    return bytes(random.getrandbits(8) for i in range(20))

def get_random_node_id():
    return bytes(random.getrandbits(8) for i in range(20))

def load_config(path):
    fd = open(path)
    config = json.loads(fd.read())
    fd.close()
    return config

def dump_node_hex(data = None):
    return codecs.decode(data.encode(), "hex")

class DelayList(object):
    def __init__(self, data = []):
        self.data = data
        self.iter = iter(self.data)

    def __iter__(self):
        return self

    def __next__(self):
        return self.iter.__next__()
