""" 메모리 사용을 추적하는 방법은 두 가지다. 81_2, 81_3 에서는
각각 gc, tracemalloc 을 이용해 메모리 사용량을 추적하는 스크립트가 들어 있다.
이 스크립트는 81_2, 81_3 에서 호출될 메모리 낭비 스크립트다.
"""

import os


class MyObject:
    def __init__(self):
        self.data = os.urandom(100)


def get_data():
    values = []
    for _ in range(10):
        obj = MyObject()
        values.append(obj)
    return values


def run():
    deep_values = []
    for _ in range(100):
        deep_values.append(get_data())
    return deep_values
