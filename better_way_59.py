""" 앞선 예제들에서는 다음과 같은 문제들이 있었다.
1. 스레드에서 발생한 예외를 잡아내기가 어려워 디버깅이 어렵다. (better_way_57)
   혹은 스레드 내에서 발생한 예외를 프로그래머가 한번 더 명시적으로 처리해야 한다. (better_way_58)
2. 스레드 생성은 무거운데, 너무 많이 생성한다. (better_way_57)
   스레드 생성량을 제한하고 큐를 사용하자니 논리가 복잡해진다. (better_way_58)
3. 싱글 스레드 구현을 재사용하기 어렵다. (better_way_58)
하지만 ThreadPoolExecutor 을 사용하면 이러한 문제들을 쉽게 해결할 수 있다.
1. 스레드 풀을 생성할 때 최대 동시작업 스레드 수를 정해 두기 때문에 메모리 고갈 문제가 없다.
2. 스레드가 필요한 시점에 만들고 실행하는 것이 아니라, 미리 만들어 두고 꺼내 써 오버헤드가 없다.
3. 스레드에서 발생한 예외를 `future.result` 메서드 호출 시 함께 전파한다.
4. 구현이 복잡하지 않아 싱글스레드 구현을 재사용하기 용이하다.
"""

from concurrent.futures import ThreadPoolExecutor

from better_way_56 import step_cell, ALIVE
from better_way_57 import LockingGrid

from utils import colorprint


def simulate_pool(
    pool: ThreadPoolExecutor,
    grid: LockingGrid
):
    h, w = grid.height, grid.width
    next_grid = LockingGrid(width=w, height=h)

    futures = []
    for y in range(h):
        for x in range(w):
            args = (y, x, grid.get, next_grid.set)
            # pool 에는 동시에 실행될 수 있는 최대 작업자(스레드) 수가
            # 정해져 있기 때문에, 풀에 남은 작업자가 없는 경우 대기한다.
            future = pool.submit(step_cell, *args)
            futures.append(future)

    for future in futures:
        # Future 클래스 인스턴스의 result 메서드는
        # 쓰레드 실행 중 나타난 예외도 모두 전파시켜준다.
        # 확인하고 싶으면 better_way_56.py 의 `io_error`
        # 파라미터를 `True`로 만들어 보자.
        future.result()

    return next_grid


if __name__ == '__main__':
    grid = LockingGrid(width=10, height=5)
    grid.set(0, 3, ALIVE)
    grid.set(1, 4, ALIVE)
    grid.set(2, 2, ALIVE)
    grid.set(2, 3, ALIVE)
    grid.set(2, 4, ALIVE)

    colorprint('게임 시작')

    with ThreadPoolExecutor(max_workers=10) as pool:
        for i in range(5):
            grid = simulate_pool(pool, grid)
            print('..')
            print(grid)
