from weakref import WeakKeyDictionary


# `__get__`과 `__set__`을 구현하는 일을
# 디스크립터 프로토콜을 구현하는 일이라고 한다.
# 디스크립터 프로토콜은 파이썬에서 애트리뷰트 접근을 해석하는 방법을 정의한다.
# @property, setter이 점점 많아지는 것 같을 때 선택을 고민해보자.
class Grade:
    def __init__(self) -> None:
        self._values = WeakKeyDictionary()
        # 여기서 WeakKeyDictionary를 사용하는 이유는
        # `self._values`에서 `Exam` 클래스 객체를 참조하고 있어
        # 발생하는 메모리 누수를 막기 위함이다.

    def __get__(self, instance, instance_type):
        # 파이썬에서는 기본적으로 객체의 멤버 변수를 조회하기 위해
        # `a.b` 와 같은 구문을 사용할 때
        # 객체 exam 의 애트리뷰트를 먼저 뒤진 다음, 발견하지 못하면
        # 클래스 Exam 의 클래스 애트리뷰트를 뒤진다.
        if instance is None:
            return self
        return self._values.get(instance, 0)

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError(
                '점수는 0과 100 사이입니다.'
            )
        self._values[instance] = value


class Exam:
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()


if __name__ == '__main__':
    first_exam = Exam()
    second_exam = Exam()

    # first_exam.writing_grade = 82 코드는
    # 다음과 같이 다시 작성해볼 수 있다.
    # Exam.__dict__['writing_grade'].__set__(exam, 82)
    first_exam.writing_grade = 82

    # Exam.__dict__['writing_grade'].__set__(exam, 82)
    second_exam.writing_grade = 75

    # print(first_exam.writing_grade) 코드는
    # 다음과 같이 다시 작성해볼 수 있다.
    # Exam.__dict__['writing_grade'].__get__(exam, Exam)
    print(f'{first_exam.writing_grade} 맞음')

    # Exam.__dict__['writing_grade'].__get__(exam, Exam)
    print(f'{second_exam.writing_grade} 맞음')
