""" 앞선 예제에서는 `ThreadPoolExecutor`을 사용하는 경우 얻을 수 있는 다양한 장점에 대해 논했다.
이번에는 `ThreadPoolExecutor`과 함께 고려해볼 수 있는 선택지인 코루틴에 대해 이야기한다.
코루틴은 쉽게 말해 실행을 일시정지할 수 있는 함수다.
책에서는 심지어 `ThreadPoolExecutor` 보다 더 나은 선택이라고 여긴다.
코루틴은 다음과 같은 장점이 있다.
1. python 이벤트 루프는 단일 스레드에서 돈다. 스레드 전환 비용이 들지 않는데 스레드 동작을 흉내낼 수 있다.
   특히, python 은 GIL 때문에 이벤트 루프를 이용하는 것이 다중 스레드를 사용하는 것에 비해 유리하다.
   락을 걸 필요가 없다.
2. 이벤트 루프는 스레드의 개수 등을 제한하는 파라미터가 없다.
   스레드에서 실행하는 작업은 매우 가벼운데 단순히 오래 걸리는 작업인 경우,
   스레드의 개수를 제한해두는 일 자체가 큰 손해를 보는 일일지도 모른다.
3. 단일 스레드에서 돌기 때문에 디버깅이 쉽다.
   `ThreadPoolExecutor`이 `future.result()`에서 예외가 발생하는 반면, 코루틴은 예외가 즉각 발생한다.
"""

import time
import typing
import asyncio

from utils import colorprint

from better_way_56 import count_neighbors, Grid


ALIVE = '*'
EMPTY = '_'


async def game_logic(
    state,
    neighbors,
    io_blocking_time: float = 0.01,
    io_error: bool = False
):
    """ 특정 셀과 해당 셀 근처에 몇 개의 이웃이 있는지를 확인하여
    해당 셀이 다음 세대에 생존할 수 있는지 판단합니다.
    """
    if io_blocking_time:
        # print('I/O Blocking ... ')
        await asyncio.sleep(io_blocking_time)
        # `time.sleep` 은 코루틴 지원을 안한다.
        # 지원을 하지 않는다는 말은, time.sleep 을 실행하는 중
        # 다른 코루틴을 실행하도록 허용하지 않는다는 이야기이다.
    if io_error:
        raise IOError

    if state == ALIVE:
        if neighbors < 2:
            return EMPTY
        elif neighbors > 3:
            return EMPTY
    else:
        if neighbors == 3:
            return ALIVE
    return state


async def step_cell(
    y: int,
    x: int,
    get: typing.Callable,
    set: typing.Callable,
) -> None:
    """ 그리드 내 특정 위치 주변의 상태를 확인한 뒤
    다음 세대의 결과에 해당 값을 반영합니다.
    """
    state = get(y, x)
    neighbors = count_neighbors(y, x, get)
    next_state = await game_logic(state, neighbors)
    set(y, x, next_state)


async def simulate(grid: Grid) -> Grid:
    h, w = grid.height, grid.width
    next_grid = Grid(width=w, height=h)

    tasks = []
    for y in range(h):
        for x in range(w):
            tasks.append(step_cell(y, x, grid.get, next_grid.set)) # 팬아웃

    await asyncio.gather(*tasks) # 팬인

    return next_grid


if __name__ == '__main__':
    grid = Grid(width=5, height=5)
    grid.set(0, 3, ALIVE)
    grid.set(1, 4, ALIVE)
    grid.set(2, 2, ALIVE)
    grid.set(2, 3, ALIVE)
    grid.set(2, 4, ALIVE)

    colorprint('게임 시작')
    s = time.time()
    print(grid)

    for i in range(5):
        grid = asyncio.run(simulate(grid)) # 코루틴 시작
        print('..')
        print(grid)

    e = time.time()
    colorprint(f'게임 끝, {e-s:.2f}초 소요됨.')
