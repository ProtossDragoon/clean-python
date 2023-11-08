""" 클래스 등록 과정을 __init_subclass__ 메서드를 이용해 자동화해 보자.
물론 메타클래스를 이용해서 동일한 작업을 수행할 수 있지만,
better way 48 에서 학습했듯 메타클래스보다 __init_subclass__ 메서드가
작성하기 쉽고 직관적이라는 장점이 있다.
"""

import json
from better_way_49_1 import Serializable


# 이 파일에서도 마찬가지로 역직렬화(문자열에서 객체로)를 위해
# 딕셔너리에 클래스를 등록하는 원시적인 방법을 사용한다.
registry = {}

def register_class(target_class):
    registry[target_class.__name__] = target_class


# 하지만 `register_class` 메서드가
# `Serializable` 클래스를 상속받는
# 모든 클래스들에 대해 자동으로 수행된다는 차이가 있다.
class ValidateRegister(Serializable):
    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        register_class(cls)

    def serialize(self):
        return json.dumps({
            'class': self.__class__.__name__,
            'args': self.args,
            'kwargs': self.kwargs,
        })


class Point2D(ValidateRegister):
    def __init__(self, x, y, a=34, b=56) -> None:
        super().__init__(x, y, a=a, b=b)
        self.x = x
        self.y = y
        self.a = a
        self.b = b


def deserialize(data):
    d = json.loads(data)
    name = d['class']
    args = d['args']
    kwargs = d['kwargs']
    target_class = registry[name]
    return target_class(*args, **kwargs)


if __name__ == '__main__':
    before = Point2D(5, 3, a=12)
    print('이전:', before)
    data = before.serialize()
    print('직렬화:', data)
    after = deserialize(data)
    print('이후:', after)
