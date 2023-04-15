"""
Модуль с криптографическими функциями:
    xor        применяет xor шифрование к значению
"""
from itertools import cycle


def xor(message: str, key: str) -> str:
    """
    XOR Шифрование

    :param message: шифруемый текст
    :param key: ключ шифрования
    :return: зашифрованный день
    """
    return "".join(chr(ord(x) ^ ord(y)) for x, y in zip(message, cycle(key)))
