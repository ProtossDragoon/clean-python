""" better way 57, 58, 59 에서는 동시성을 설명하기 위해 이 코드를 기반삼아 이용한다.
팬아웃(fan-out)은 동시에 실행되는 여러 실행 흐름을 만들어내는 과정을 의미한다.
팬인(fan-in)은 동시 작업 단위의 작업이 모두 끝날 때까지 기다리는 과정을 의미한다.
"""

import typing
import time

from utils import colorprint


ALIVE = '*'
EMPTY = '_'

class Grid:
    def __init__(
        self, /, *,
        width: int = 0,
        height: int = 0,
    ):
        assert width > 0 and height > 0
        self.width = width
        self.height = height
        self.rows = []
        for _ in range(self.height):
            self.rows.append([EMPTY] * self.width)

    def get(self, y, x):
        return self.rows[y % self.height][x % self.width]

    def set(self, y, x, state):
        assert state in [ALIVE, EMPTY]
        self.rows[y % self.height][x % self.width] = state

    def __str__(self) -> str:
        lines = []
        for row in self.rows:
            line = ''.join(row)
            lines.append(line)
        return '\n'.join(lines)


def count_neighbors(
    y: int,
    x: int,
    get: typing.Callable,
) -> int:
    n_ = get(y - 1, x + 0)
    ne = get(y - 1, x + 1)
    e_ = get(y + 0, x + 1)
    se = get(y + 1, x + 1)
    s_ = get(y + 1, x + 0)
    sw = get(y + 1, x - 1)
    w_ = get(y + 0, x - 1)
    nw = get(y - 1, x - 1)
    neighbor_states = [n_, ne, e_, se, s_, sw, w_, nw]

    count = 0
    for state in neighbor_states:
        if state == ALIVE:
            count += 1
    return count


def game_logic(
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
        time.sleep(io_blocking_time)
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


def step_cell(
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
    next_state = game_logic(state, neighbors)
    set(y, x, next_state)


def simulate(grid: Grid) -> Grid:
    h, w = grid.height, grid.width
    next_grid = Grid(width=w, height=h)
    for y in range(h):
        for x in range(w):
            step_cell(y, x, grid.get, next_grid.set)
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
        grid = simulate(grid)
        print('..')
        print(grid)

    e = time.time()
    colorprint(f'게임 끝, {e-s:.2f}초 소요됨.')
