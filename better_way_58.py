""" `Queue` (better_way_55_2) 를 사용하면 better_way_57 에 나타났던 문제들이 해결된다.
1. 스레드에서 발생한 예외들은 모두 `Queue` 내부에 저장되기 때문에 처리하기 용이하다.
2. 무한정 많은 스레드가 생성되지 않아 메모리와 CPU 오버헤드가 적다.
성능을 제외하고 가장 큰 장점은 기존의 싱글 스레드 구현을 그대로 사용할 수 있다는 점이다.
better_way_57 과 같이 스레드 락을 이용한 그리드 자식 클래스를 정의할 필요가 없어진다.
물론 이 방식도 문제점들을 가지고 있다.
1. `simulate_pipeline` 은 `simulate`함수(better_way_56)는 물론, `simulate_threaded` 함수(better_way_57)보다도 어렵다.
2. `BetterQueue`, `StoppableWorker` 이라는 추가적인 구현체들이 필요하다.
3. better_way_57 과 달리, 실행되는 스레드의 개수가 늘어났다 뿐이지 고정되어 있다.
4. 예외를 잡아 처리할 수는 있지만 예외를 꼬박꼬박 큐에 넣어 주어야 하고 메인 스레드에서 다시 확인해야 한다.
5. 요구사항 변경에 대응이 어렵다.
"""

import time
from threading import Thread

from better_way_55_2 import BetterQueue, StoppableWorker
from better_way_56 import game_logic, count_neighbors, Grid, ALIVE
from utils import colorprint


def game_logic_thread(item):
    y, x, state, neighbors = item
    try:
        # `game_logic` 은 싱글스레드 구현임.
        next_state = game_logic(state, neighbors)
    except Exception as e:
        next_state = e
    return (y, x, next_state)


class SimulationError(Exception):
    pass


def simulate_pipeline(
    grid: Grid, # `Grid` 는 싱글스레드 구현임.
    in_queue: BetterQueue,
    out_queue: BetterQueue,
):
    # 멀티 스레드를 고려하지 않고 만들어진 `Grid` 클래스를 그대로 사용할 수 있는 이유는
    # `Grid` 클래스에서 경합조건이 발생할 수 있는 부분인 `get` 메서드와 `set` 메서드가
    # 스레드 내부에서 호출되지 않고, 단일 스레드에서 실행되는 이 함수에서만 호출되기 때문이다.
    h, w = grid.height, grid.width
    for y in range(h):
        for x in range(w):
            state = grid.get(y, x)
            neighbors = count_neighbors(y, x, grid.get)
            in_queue.put((y, x, state, neighbors)) # 팬아웃

    # 동시적으로 처리해야 하는 작업들이 모두 할당이 완료된다.
    # 빈 큐가 될 때까지 원소를 모두 소비하는 작업을 수행한다.
    in_queue.join()

    # `out_queue` 에는 처리가 완료된 순서대로 원소가 차고 있을 것이다.
    # 가장 뒤에 센티넬을 추가해 준다.
    out_queue.close()

    next_grid = Grid(height=h, width=w)
    for item in out_queue:
        y, x, next_state = item
        if isinstance(next_state, Exception):
            # 스레드 내부에서 발생한 예외들도 큐에 담겨 오기 때문에 모두 잡아낼 수 있다.
            raise SimulationError(y, x) from next_state
        next_grid.set(y, x, next_state)

    return next_grid


def pipe_ready(
    n_thread: int,
    in_queue: BetterQueue,
    out_queue: BetterQueue,
) -> list[Thread]:
    threads = []
    for _ in range(n_thread):
        thread = StoppableWorker(
            game_logic_thread,
            in_queue=in_queue,
            out_queue=out_queue
        )
        thread.start()
        threads.append(thread)
    return threads


if __name__ == '__main__':
    grid = Grid(width=5, height=5)
    grid.set(0, 3, ALIVE)
    grid.set(1, 4, ALIVE)
    grid.set(2, 2, ALIVE)
    grid.set(2, 3, ALIVE)
    grid.set(2, 4, ALIVE)

    colorprint('게임 시작')

    in_queue = BetterQueue(5)
    out_queue = BetterQueue(5000)
    # NOTE: out_queue 의 크기가 큰 이유는
    # 현재 구조상 input 이 모두 처리되면 output 이 처리되는 구조이기 때문이다.
    # 만약 out_queue 가 width * height 를 모두 담지 못하면 데드락이 발생한다.

    # 생산자-소비자 큐에 기반하여 동작하는 스레드를 미리 시작해둔다.
    threads = pipe_ready(
        n_thread=5,
        in_queue=in_queue,
        out_queue=out_queue
    )

    s = time.time()
    print(grid)

    for i in range(5):
        grid = simulate_pipeline(
            grid,
            in_queue=in_queue,
            out_queue=out_queue
        )
        print('..')
        print(grid)

    for thread in threads:
        in_queue.close()
    for thread in threads:
        thread.join()

    e = time.time()
    colorprint(f'게임 끝, {e-s:.2f}초 소요됨.')
