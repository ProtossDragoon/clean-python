""" `__getattribute__` 나 `__setattr__` 메서드 내부에서
애트리뷰트에 다시 접근하는 경우 문제가 발생할 수 있다.
이들은 애트리뷰트에 접근할 때마다 다시 호출되기 때문이다!
"""

class BrokenDictionaryRecord():
    def __init__(self) -> None:
        self._data = {}

    def __getattribute__(self, name):
        return self._data[name] # 여기에서 __getattribute__ 가 다시 실행된다.

# 위 클래스는 무한 재귀 문제를 가지고 있다.
# 아래와 같이 수정하면 문제를 해결할 수 있다.
class DictionaryRecord():
    def __init__(self) -> None:
        self._data = {
            'foo': '존재하는 키 `foo`에 대한 값'
        }

    def __getattribute__(self, name):
        try:
            # 아래는 인스턴스 애트리뷰트 딕셔너리, 즉 `__dict__`에서 값을 가져온다.
            return super().__getattribute__('_data')[name]
        except:
            raise AttributeError(f'`{name}`을 찾을 수 없음.')


if __name__ == '__main__':
    # data = BrokenDictionaryRecord()
    data = DictionaryRecord()
    print('foo:', data.foo)

    try:
        print('bar:', data.bar)
    except AttributeError as e:
        print(e)

    try:
        print('__dict__:', data.__dict__)
    except AttributeError as e:
        # `__getattribute__` 메서드에서는 항상
        # `__dict__`의 `_data` 만을 탐색하므로
        # `__dict__` 조차 찾을 수 없다.
        print(e)
