""" 클래스의 각 멤버 함수에 대해 데코레이터를 사용하고 싶다면,
각 멤버 함수에 명시적으로 데코레이터를 호출할 수 있다. 하지만 이 방법은 번거롭다.
당연히 자식 클래스에서 새롭게 정의한 함수들에 대해서는 데코레이터 실행을 보장할 수 없다.
그 대신, 메타클래스를 이용할 수 있다.
"""

import time
import types
from functools import wraps

from utils import colorprint


def trace_fn(fn):
    # 데코레이터를 한 번만 적용하기 위해 사용하는 구문
    # 이 예제에서는 이 구문을 사용하지 않는 경우
    # 몇 번 실행되는지를 보여주기 위해 `tracing` 이라는 이름의
    # 사용하지 않는 애트리뷰트를 가지고 있는지를 검사함
    if hasattr(fn, 'tracing'):
        return fn

    @wraps(fn)
    def wrapper(*args, **kwargs):
        s = time.time()
        ret = fn(*args, **kwargs)
        e = time.time()
        print(f'`{fn.__name__}()` {e - s:.7f} 초')
        return ret

    return wrapper


# 각각이 어떤 것을 의미하는지는 나중에 확인해도 됨.
# 내가 정의한 메서드들이 `MethodType` 이 아니라 `FunctionType으로` 잡히는 등
# 아직까지는 예상과 다르게 작동하는 느낌임.
# 이런 것들이 있지만, 이 예제를 돌리기 위해서는 `types.FunctionType` 이면 충분하다.
# 자세한 내용은 https://docs.python.org/ko/3/library/types.html 참고.
trace_types = (
    # types.MethodType,
    types.FunctionType,
    types.BuiltinFunctionType,
    # types.MethodDescriptorType,
    # types.ClassMethodDescriptorType
)


class TraceMeta(type):
    def __new__(meta, name, bases, class_dict):
        klass = super().__new__(meta, name, bases, class_dict)

        for key in dir(klass):
            value = getattr(klass, key)
            if isinstance(value, trace_types):
                # print(f'데코레이팅: (클래스: {klass.__name__}) `{key}`')
                wrapped = trace_fn(value)
                setattr(klass, key, wrapped)

        return klass


class TraceClass(metaclass=TraceMeta):
    def __getattr__(self, name):
        if name == 'a':
            return ''
        raise AttributeError(f'`{name}`을 찾을 수 없음.')

    def run(self):
        i = 0
        for _ in range(100):
            i += 1

    @staticmethod
    def static_run():
        i = 0
        for _ in range(100):
            i += 1


class TraceChildrenClass(TraceClass):
    def child_run(self):
        i = 0
        for _ in range(1000):
            i += 1

    @staticmethod
    def child_static_run():
        i = 0
        for _ in range(1000):
            i += 1


if __name__ == '__main__':
    # 데코레이터는 생성자에도 적용되고,
    colorprint('\n객체 생성')
    trace_class = TraceClass()
    # "1회" 출력됨

    # 메서드에도 적용되고,
    colorprint('\n`run()` 호출')
    trace_class.run()
    # "1회" 출력됨

    # 정적 메서드에도 적용되고,
    colorprint('\n`static_run()` 호출')
    TraceClass.static_run()
    # "1회" 출력됨

    # 이렇게 메서드에 접근할 때 훅을 걸수도 있다.
    colorprint('\n애트리뷰트 접근')
    trace_class.a
    # "1회" 출력됨

    # 자식 클래스
    colorprint('\n자식 클래스 객체 생성')
    trace_child_class = TraceChildrenClass()
    # ""2회"" 출력됨

    colorprint('\n자식 클래스: `run()` 호출')
    trace_child_class.run()
    # ""2회"" 출력됨

    colorprint('\n자식 클래스: `child_run()` 호출')
    trace_child_class.child_run()
    # "1회" 출력됨

    colorprint('\n자식 클래스: `static_run()` 호출')
    TraceChildrenClass.static_run()
    # ""2회"" 출력됨

    colorprint('\n자식 클래스: `child_static_run()` 호출')
    TraceChildrenClass.child_static_run()
    # "1회" 출력됨

    colorprint('\n자식 클래스: 애트리뷰트 접근')
    trace_child_class.a
    # ""2회"" 출력됨
