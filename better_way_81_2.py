""" 가장 간단한 `gc` 내장 모듈을 이용한 방법이다.
"""

import gc

from utils import colorprint
import better_way_81_1 as waste_memory


if __name__ == '__main__':
    found_objects = gc.get_objects()
    colorprint('이전:', len(found_objects))
    hold_reference = waste_memory.run()
    print('`hold_reference` 변수가 참조값을 들고 있음.')
    found_objects = gc.get_objects()
    colorprint('이후:', len(found_objects))

    for obj in found_objects:
        print('얻을 수 있는 정보:', repr(obj))
        break
