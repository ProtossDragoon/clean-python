""" 메타클래스를 사용하여 구현하는 경우 메타클래스의 한계들을 그대로 가진다.
그 대신, 클래스 데코레이터를 이용하라.
클래스 데코레이터는 메타클래스를 이용하는 방법과 달리, 자식 클래스에서 데코레이터 실행을 보장하지 않는다.
하지만 클래스를 합성해야 하는 경우 오히려 유용할 수 있다.
예를 들어, A 클래스에 데코레이터 a, B 클래스에 데코레이터 b 를 사용하고,
C 클래스에서 A 클래스와 B 클래스를 모두 상속받아 클래스를 합성하고자 하는 경우 유용하다.
메타클래스는 하나만 지정할 수 있고, 여러 개를 지정하는 기교를 부리더라도 코드가 난잡해지기 때문이다.
"""

from better_way_51_1 import trace_fn, trace_types

from utils import colorprint


def trace(klass):
    for key in dir(klass):
        value = getattr(klass, key)
        if isinstance(value, trace_types):
            # print(f'데코레이팅: (클래스: {klass.__name__}) `{key}`')
            wrapped = trace_fn(value)
            setattr(klass, key, wrapped)
    return klass


@trace
class TraceClass2():
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


class TraceChildrenClass2(TraceClass2):
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
    trace_class = TraceClass2()
    # "1회" 출력됨

    # 메서드에도 적용되고,
    colorprint('\n`run()` 호출')
    trace_class.run()
    # "1회" 출력됨

    # 정적 메서드에도 적용되고,
    colorprint('\n`static_run()` 호출')
    TraceClass2.static_run()
    # "1회" 출력됨

    # 이렇게 메서드에 접근할 때 훅을 걸수도 있다.
    colorprint('\n애트리뷰트 접근')
    trace_class.a
    # "1회" 출력됨

    # 자식 클래스
    colorprint('\n자식 클래스 객체 생성')
    trace_child_class = TraceChildrenClass2()
    # "1회" 출력됨

    colorprint('\n자식 클래스: `run()` 호출')
    trace_child_class.run()
    # "1회" 출력됨

    colorprint('\n자식 클래스: `child_run()` 호출')
    trace_child_class.child_run()

    colorprint('\n자식 클래스: `static_run()` 호출')
    TraceChildrenClass2.static_run()
    # "1회" 출력됨

    colorprint('\n자식 클래스: `child_static_run()` 호출')
    TraceChildrenClass2.child_static_run()

    colorprint('\n자식 클래스: 애트리뷰트 접근')
    trace_child_class.a
    # "1회" 출력됨
