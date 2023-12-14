""" `gc`를 이용한 방법은 정확히 어떤 부부넹서 메모리를 사용했는지 알기 어렵다.
반면 `tracemalloc` 내장 모듈을 이용하면 스택 트레이스를 추적할 수 있다.
파일 이름 단위, 라인 단위로 메모리를 많이 차지하는 부분을 쉽게 출력해볼 수 있다.
"""

import tracemalloc

from utils import colorprint
import better_way_81_1 as waste_memory


if __name__ == '__main__':
    tracemalloc.start(10)
    time1 = tracemalloc.take_snapshot()
    hold_reference = waste_memory.run() # 찰칵
    colorprint('`hold_reference` 변수가 참조값을 들고 있음.')
    time2 = tracemalloc.take_snapshot() # 찰칵

    # key_type 별로 그룹화된 Statistic 인스턴스의 정렬된 리스트로 통계를 가져올 수 있다.
    stats = time2.compare_to(time1, 'lineno') # 'lineno': 파일명과 줄 번호
    for stat in stats[:5]:
        print(stat)

    stats = time2.compare_to(time1, 'traceback') # 'traceback' 트레이스백
    colorprint('메모리를 가장 많이 사용하는 부분은: ')
    top1 = stats[0]
    print(f'\n'.join(top1.traceback.format()))
