from itertools import cycle


def xor(message, key):
    return "".join(chr(ord(x) ^ ord(y)) for x, y in zip(message, cycle(key)))