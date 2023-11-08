""" 클래스를 등록하는 일이란 무엇일까?
대상이 어떤 종류의 클래스이든 상관없이, 이런 클래스가 있어요~ 를 어느 컨테이너에
담아 두는 것을 클래스 등록이라고 한다. 이 클래스 등록이 자동화되지 않으면,
개발자가 항상 명시적으로 등록을 해 주어야 한다. 등록이 자동화되지 않은 예시를 먼저 보자.
"""

import json


# 클래스를 등록하는 일과 관련된 작업의 대표적인 예시로,
# 객체의 직렬화와 역직렬화가 있다. 객체를 생성하려면 기본적으로
# 클래스에 대한 정보와 클래스에 저장된 값들에 대한 정보가 필요하다.
# 하지만 직렬화가 되는 순간 클래스로서의 의미는 사라지고 문자열만 남는 셈이다.
# 문자열에서 클래스를 다시 찾아내는 방법은 무엇일까?
# 이 파일에서는 역직렬화(문자열에서 객체로)를 위해
# 딕셔너리에 클래스를 등록하는 원시적인 방법을 사용한다.
registry = {}

def register_class(target_class):
    registry[target_class.__name__] = target_class


class Serializable():
    def __init__(self, *args, **kwargs) -> None:
        self.args = args
        self.kwargs = kwargs

    def serialize(self):
        return json.dumps({
            'class': self.__class__.__name__,
            'args': self.args,
            'kwargs': self.kwargs,
        })

    def __repr__(self) -> str:
        name = self.__class__.__name__
        args_str = ', '.join(str(x) for x in self.args)
        kwargs_str = ', '.join(
            f'{str(k)}={str(v)}' for k, v in self.kwargs.items()
        )
        return f'{name}({args_str}, {kwargs_str})'


class Point2D(Serializable):
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
    register_class(Point2D) # 명시적으로 호출해야 한다는 문제가 있음.
    after = deserialize(data)
    print('이후:', after)
