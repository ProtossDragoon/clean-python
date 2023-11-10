""" 현재 상황은 Customer 클래스에서 데이터를 담는 필드들이 있을 때
이 필드들을 객체로 관리하려고 하는 상황이다.
이때, 필드마다 동일한 객체가 할당되는데, 이 객체의 이름을 자동적으로
필드 객체를 저장하는 변수의 이름으로 설정하고 싶으면 어떻게 해야 할까?
"""

class Field():
    def __init__(self) -> None:
        self.name = None
        self.internal_name = None

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return getattr(instance, self.internal_name, '')

    def __set__(self, instance, value):
        setattr(instance, self.internal_name, value)


class Meta(type):
    def __new__(_meta, _name, _bases, class_dict):
        for k, v in class_dict.items():
            # k: 클래스 애트리뷰트의 변수 이름
            # v: 클래스 애트리뷰트 `k` 에 저장된 값
            if isinstance(v, Field):
                v.name = k
                v.internal_name = '_' + k
        cls = type.__new__(_meta, _name, _bases, class_dict)
        return cls


class Customer(metaclass=Meta):
    email = Field()
    first_name = Field()
    last_name = Field()


if __name__ == '__main__':
    customer = Customer()

    # Customer.__dict__['email'].__get__(customer, Customer)
    print(f'값 할당 이전: {customer.email!r} ({customer.__dict__})')
    customer.email = 'hello@world.com'
    print(f'값 할당 이후: {customer.email!r} ({customer.__dict__})')

    # Customer.__dict__['first_name'].__get__(customer, Customer)
    print(f'값 할당 이전: {customer.first_name!r} ({customer.__dict__})')
    customer.first_name = 'ProtossDragoon'
    print(f'값 할당 이후: {customer.first_name!r} ({customer.__dict__})')
