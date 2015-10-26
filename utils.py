from os.path import commonprefix as commonPrefix
import random

def get_echo_bytes():
    return bytes(random.getrandbits(8) for i in range(4))
