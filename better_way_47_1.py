""" 어떤 클래스 안에 __getattr__ 메서드 정의가 있으면,
이 객체의 인스턴스 딕셔너리(__dict__)에서 찾을 수 없는 애트리뷰트에 접근할 때마다
__getattr__ 이 호출된다.
"""

class LazyRecord():
    def __init__(self) -> None:
        self.exists = 5

    def __getattr__(self, name):
        value = f'정의되지 않은 `{name}`를 위한 값'
        setattr(self, name, value)
        return value


if __name__ == '__main__':
    data = LazyRecord()
    print('이전:', data.__dict__)
    print('foo:', data.foo)
    print('이후:', data.__dict__)
