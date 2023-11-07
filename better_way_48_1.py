""" 메타클래스는 type을 상속해 정의된다.
메타클래스는 클래스 이름, 클래스의 부모 클래스들, 모든 클래스 애트리뷰트에 접근할 수 있다.
"""

class ValidatePolygon(type):
    def __new__(meta, name, bases, class_dict):
        if bases: # 하위 클래스만 검증한다. 하위 클래스가 아닌 경우 bases 변수에는 빈 튜플이 들어 있다.
            if class_dict['sides'] < 3:
                raise ValueError('다각형의 변은 최소 3개입니다.')
        return type.__new__(meta, name, bases, class_dict)


class Polygon(metaclass=ValidatePolygon):
    sides = None

    @classmethod
    def interior_angles(cls):
        return (cls.sides - 2) * 180


if __name__ == '__main__':
    class Rectangle(Polygon):
        sides = 4

    try:
        class Line(Polygon):
            sides = 1
    except ValueError as e:
        print(e)
