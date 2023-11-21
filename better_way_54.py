""" GIL이 있다는 말이 인터럽트를 정직하게 하겠다는 것은 아니다.
인터럽트는 어느 순간에든 들어올 수 있다. 값을 읽어 가는 과정에서도 마찬가지다.
파이썬 3.10 패치에서 몇몇 특수하고 단순한 연산들에 대해 GIL의 한계를 극복할 수 있는 최적화 작업이 있었다.
따라서 단순히 += 1 을 하는 방식으로는 데이터 경합 상태를 만들 수 없어서,
int(str()) 과 같은 강제 캐스팅으로 해당 기능이 정상적으로 작동하지 않도록 망쳐 두었다.
이러한 데이터 경합을 막기 위해 `Lock`  사용하라. 하지만 `Lock`을 사용하면 속도가 확연히 느려진다.
"""

import time
from threading import Lock, Thread

from utils import colorprint


class UnLockingCounter:
    def __init__(self) -> None:
        self.count = 0

    def increment(self, offset) -> None:
        self.count += int(str(offset))


class LockingCounter:
    def __init__(self) -> None:
        self.lock = Lock()
        self.count = 0

    def increment(self, offset) -> None:
        with self.lock:
            self.count += int(str(offset))


def worker(how_many, counter):
    for _ in range(how_many):
        counter.increment(1)


n_thread = 20
how_many = 10 ** 6

# 스레드를 `n_thread`개 실행하므로
# 최종적으로 얻어야 하는 값은 (`n_thread`x`how_many`)다.
expected = n_thread * how_many


def trial(counter):
    s = time.time()
    for _ in range(n_thread):
        for _ in range(how_many):
            counter.increment(1)
    e = time.time()

    found = counter.count
    print(f'카운터 값은 {expected}이어야 하지만 {found}를 얻었습니다. '
          f'{e-s:.4f}초가 소요되었습니다.')


def threading_trial(counter):
    threads = []
    for i in range(n_thread):
        # 동시적으로 worker 스레드를 실행한다.
        thread = Thread(
            target=worker,
            args=(how_many, counter)
        )
        threads.append(thread)
        thread.start()

    # 스레드가 값을 다 읽을 때까지 기다린다.
    s = time.time()
    for thread in threads:
        thread.join()
    e = time.time()

    found = counter.count
    print(f'카운터 값은 {expected}이어야 하지만 {found}를 얻었습니다. '
          f'{e-s:.4f}초가 소요되었습니다.')


if __name__ == '__main__':

    colorprint('`Lock` 없는 카운터, 싱글 스레드로 실행')
    broken_counter = UnLockingCounter()
    trial(broken_counter)

    colorprint('`Lock` 있는 카운터, 싱글 스레드로 실행')
    counter = LockingCounter()
    trial(counter)

    colorprint(f'`Lock` 없는 카운터, 멀티({n_thread}개) 스레드로 실행')
    broken_counter = UnLockingCounter()
    threading_trial(broken_counter)

    colorprint(f'`Lock` 있는 카운터, 멀티({n_thread}개) 스레드로 실행')
    counter = LockingCounter()
    threading_trial(counter)
