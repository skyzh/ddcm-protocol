import random
import json
import codecs

from os.path import commonprefix as commonPrefix

def get_echo_bytes():
    return bytes(random.getrandbits(8) for i in range(4))

def get_random_node_id():
    return bytes(random.getrandbits(8) for i in range(20))

def load_config(path):
    fd = open(path)
    config = json.loads(fd.read())
    fd.close()
    return config

def dump_node_hex(data = None):
    return data or codecs.decode(data.encode(), "hex")
