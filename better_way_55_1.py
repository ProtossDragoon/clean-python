""" 블로킹 I/O가 있는 작업들을 반복적으로 처리해야 할 때, 파이프라인을 구축할 수 있다.
파이프라인을 구축할 때에는 스레드를 이용하고 생산자-소비자 큐를 이용하면 좋다.
하지만 효율적인 생산자-소비자 큐를 만드는 일은 간단하지 않다.
아래 소스코드는 모범적이지 못한 구현의 예시다.
"""

import time
from collections import deque
from threading import Thread, Lock, Event

from utils import colorprint


class MyQueue:
    def __init__(self) -> None:
        self.items = deque()
        self.lock = Lock()

    def put(self, item):
        with self.lock:
            self.items.append(item)

    def get(self):
        with self.lock:
            return self.items.popleft()


class Worker(Thread):
    def __init__(self, func, in_queue, out_queue):
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.polled_count = 0
        self.work_done = 0
        self.event = Event() # 스레드 종료를 위해 사용

    def run(self):
        while True:
            self.polled_count += 1
            try:
                item = self.in_queue.get()
            except IndexError:
                # 이 구현의 첫 번째 문제는 이 IndexError이 계속 발생한다는 것이다.
                # 예외를 잡아내며 무의미한 루프를 돈다는 것은 자원이 아깝게 낭비되고 있다는 뜻이다.
                # 실제로 1000개의 아이템을 처리하기 위해 3000번이 넘게 while문을 돌았다.
                # 약 2000번이 IndexError을 잡아내는 작업을 처리하기 위해 사용되었다.
                # 이는 파이프라인을 구성하는 작업자 함수의 속도가 다르기 때문에 발생한다.
                # 뒤에 있는 단계의 진행을 방해하게 된다.
                # 뒤에 있는 단계를 처리할 스레드/프로세스에게 먹거리(작업)가 주어지지 않는 상태를
                # 기아(starvation) 상태라고 한다.
                time.sleep(0.0001)
            else:
                result = self.func(item)
                self.out_queue.put(result)
                self.work_done += 1
            if self.event.is_set():
                break


def step1_download(item):
    time.sleep(0.001)
    return item


def step2_resize(item):
    time.sleep(0.001)
    return item


def step3_upload(item):
    time.sleep(0.001)
    return item


if __name__ == '__main__':
    download_queue = MyQueue()
    reszie_queue = MyQueue()
    upload_queue = MyQueue()
    done_queue = MyQueue()
    threads = [
        Worker(step1_download, download_queue, reszie_queue),
        Worker(step1_download, reszie_queue, upload_queue),
        Worker(step1_download, upload_queue, done_queue),
    ]

    for thread in threads:
        thread.start()

    colorprint('큐에 데이터 입력, 시간 측정 시작')
    t_start = time.time()

    # 데이터를 입력한다.
    for _ in range(1000):
        download_queue.put(object())

    # 작업이 끝나기를 기다린다.
    while len(done_queue.items) < 1000:
        # 이 구현의 두 번째 문제다.
        # 작업이 제대로 완료되었는지를 검사하기 위해 바쁜 대기(busy waiting)을 수행한다.
        # 현재 구현대로라면 작업자 스레드에게 루프를 중단할 시점임을 알려줄 방법이 없다.
        pass

    # 스레드 종료
    for thread in threads:
        thread.event.set()
        thread.join()

    t_end = time.time()
    colorprint('모든 스레드들의 조인 완료, 시간 측정 끝')

    processed = len(done_queue.items)
    polled = sum(worker.polled_count for worker in threads)
    print(f'{processed}개의 아이템을 처리하기 위해, '
          f'폴링을 {polled}번 수행했습니다.')
    print(f'총 처리 시간은 {t_end-t_start:3f}초 입니다.')

# 이 구현의 마지막 문제는, 파이프라인의 진행이 막히는 경우다.
# 파이프라인의 일부가 작업을 제대로 처리하지 못하면 스레드를 연결하는 큐들 중 일부가
# 지나치게 많은 데이터들을 가지며 팽창하다가 OOM으로 프로그램이 종료될지도 모른다.
