""" better way 56 의 game_logic 과 같은 함수에 io blocking 이 추가된다고 해 보자.
1개의 io blocking 당 t초가 소요된다면, `grid.width` * `grid.height` * t 초가 걸린다.
이를 해결하기 위해 떠올릴 수 있는 가장 쉬운 방법은 스레드를 이용하는 것이다.
하지만 이렇게 스레드를 사용하는 방법에는 여러 가지 문제도 있다. 이는 특히 정말 많은 수의 스레드를 만들어내야 할 때
비로소 수면 위로 올라온다. 이러한 상황을 '높은 동시성'이 요구되는 상황이라고 한다.
1. 스레드에서 발생한 예외를 잡아내기가 어려워 디버깅이 어렵다.
   예외 트레이스는 출력되지만, `join()` 부분에서 코드가 중단되지 않고 실행된다.
   이는 스레드 클래스가 target 함수에서 발생하는 예외를 독립적으로 잡아내서 `sys.stderr` 로 트레이스를 출력하기 때문이다.
   이렇게 처리되는 예외는 스레드를 호출한 쪽으로 다시 던져지지 않는다. 그래서 이를 잡아내기가 어렵다는 것이다.
2. 스레드 생성이 저렴하다고 알려져 있으나 스레드 하나당 MB 단위의 메모리를 요구하고, 시간도 오래 걸린다.
"""

import time
from threading import Thread, Lock

from better_way_56 import step_cell, Grid, ALIVE
from utils import colorprint


class LockingGrid(Grid):
    """ 그리드가 가지고 있는 셀 상태들을
    동시에 읽고 쓸 수 없도록 제한하는 그리드입니다.
    """
    def __init__(
        self, /, *,
        width: int = 0,
        height: int = 0
    ):
        super().__init__(width=width, height=height)
        self.lock = Lock()

    def get(self, y, x):
        with self.lock:
            return super().get(y, x)

    def set(self, y, x, state):
        with self.lock:
            return super().set(y, x, state)

    def __str__(self):
        with self.lock:
            return super().__str__()


def simulate_threaded(grid: LockingGrid):
    h, w = grid.height, grid.width
    next_grid = LockingGrid(width=w, height=h)

    threads = []
    for y in range(h):
        for x in range(w):
            args = (y, x, grid.get, next_grid.set)
            thread = Thread(target=step_cell, args=args)
            thread.start()
            threads.append(thread)

    for thread in threads:
        thread.join()

    return next_grid


if __name__ == '__main__':
    grid = LockingGrid(width=10, height=10)
    # 만약 작동하지 않는 모습을 보고싶다면, width 와 height 각각을 100 이상으로 설정하고
    # better_way_56.py 의 io_blocking_time 파라미터를 1 이상으로 충분히 크게 설정한 뒤
    # 다시 실행해보자. 더 이상 쓰레드를 생성할 수 없다는 경고를 확인할 수 있을 것이다.

    grid.set(0, 3, ALIVE)
    grid.set(1, 4, ALIVE)
    grid.set(2, 2, ALIVE)
    grid.set(2, 3, ALIVE)
    grid.set(2, 4, ALIVE)

    colorprint('게임 시작')
    s = time.time()
    print(grid)

    for i in range(5):
        grid = simulate_threaded(grid)
        print('..')
        print(grid)

    e = time.time()
    colorprint(f'게임 끝, {e-s:.2f}초 소요됨.')
