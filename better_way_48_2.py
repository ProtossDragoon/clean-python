""" 메타클래스는 하나만 등록할 수 있다는 문제가 있다.
메타클래스를 여러 개 등록하기 위해서는 클래스의 의미를 희생해야 할지도 모른다.
단순한 기능을 수행하기 위해 코드가 크게 더러워지고 이해하기 어려워진다.
(이펙티브 파이썬 2판의 실습 예제에서 `sides` 검증은 아예 동작하지도 않는다!)
python 3.6 에서부터는 `__init_subclass__` 메서드를 제공한다.
`__init_subclass__` 메서드를 이용하면 메타클래스가 필요없다.
보일러플레이트가 줄어들고, 여러 클래스에 대해 검증할 수 있다.
"""

class Polygon2:
    sides = None

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        if cls.sides < 3:
            raise ValueError('다각형의 변은 최소 3개입니다.')


class Filled2:
    color = None

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        if cls.color not in ('red', 'green', 'blue'):
            raise ValueError(f'`{cls.color}`은 지원하지 않는 색상입니다.')


class RedTriangle(Filled2, Polygon2):
    color = 'red'
    sides = 3


try:
    class PurpleSquare(Filled2, Polygon2):
        color = 'purple'
        sides = 4
except ValueError as e:
    print(e)
