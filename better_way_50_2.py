""" 동일한 작업을 더 쉽고 직관적인 `__set_name__` 메서드로 처리할 수 있다.
"""

class Field():
    def __init__(self) -> None:
        self.name = None
        self.internal_name = None

    def __set_name__(self, owner, name):
        # 클래스가 생성될 때, 모든 디스크립터에 대해 이 메서드가 호출된다.
        self.name = name
        self.internal_name = '_' + name

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return getattr(instance, self.internal_name, '')

    def __set__(self, instance, value):
        setattr(instance, self.internal_name, value)


class Customer():
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
