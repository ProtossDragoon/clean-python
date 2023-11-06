""" 운영 체제나 응용 소프트웨어 등의 각종 컴퓨터 프로그램에서
소프트웨어 구성 요소 간에 발생하는 함수 호출, 메시지, 이벤트 등을
중간에서 바꾸거나 가로채는 명령, 방법을 훅(hook) 이라고 한다.
여기서 나오는 `__getattr__`은 물론
앞으로 배울 `__getattribute__`, `__setattr__`도
객체에서 일어나는 훅이므로, 오브젝트 훅이라고 부른다.
"""

from utils import colorprint
from better_way_47_1 import LazyRecord


class LoggingLazyRecord(LazyRecord):
    def __getattr__(self, name):
        print(f'* `__getattr__({name})` 호출됨.')
        if name == 'bad_name':
            raise AttributeError(f'`{name}`을 찾을 수 없음.')
        result = super().__getattr__(name)
        print(f'* `{result}` 반환받음.')
        return result


if __name__ == '__main__':
    data = LoggingLazyRecord()
    colorprint('처음 상태:', data.__dict__)
    colorprint('첫번째 foo 호출:', data.foo)
    colorprint('그 이후:', data.__dict__)

    # 두 번째 foo 접근 시에는
    # 이미 foo 가 `__dict__`에 포함되어 있으므로
    # `__getattr__`이 호출되지 않는다.
    colorprint('두번째 foo 호출:', data.foo)
    colorprint('그 이후:', data.__dict__)
    print('-----------------------')

    # 평소에 자주 사용하는 `hasattr` 함수도 __dict__ 를 탐색한 뒤
    # 그 다음에는 `__getattr__` 을 호출한다.
    colorprint('foo 가 있나:', hasattr(data, 'foo'))
    colorprint('bar 가 있나:', hasattr(data, 'bar'))
    colorprint('bad_name 가 있나:', hasattr(data, 'bad_name'))
