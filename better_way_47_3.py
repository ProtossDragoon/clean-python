""" `__getattribute__`은 애트리뷰트 이름마다
한 번만 실행되는 `__getattr__`과 달리 매번 실행된다는 차이점이 있다.
`__setattr__`도 매번 실행된다.
"""

from utils import colorprint


class ValidatingRecord:
    def __init__(self) -> None:
        self.exists = 5

    def __getattribute__(self, name):
        print(f'* `__getattribute__({name})` 호출됨.')
        try:
            value = super().__getattribute__(name)
            print(f'* `{name}` 찾음, `{value}` 반환받음.')
            return value
        except AttributeError:
            value = f'정의되지 않은 `{name}`를 위한 값'
            print(f'* `{name}` 에 `{value}` 할당.')
            setattr(self, name, value)
            return value


if __name__ == '__main__':
    data = ValidatingRecord()
    colorprint('이전:', data.__dict__)
    colorprint('첫번째 foo 호출:', data.foo)
    colorprint('이후:', data.__dict__)
    colorprint('두번째 foo 호출:', data.foo)
