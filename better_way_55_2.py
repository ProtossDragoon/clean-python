import time
from queue import Queue
from threading import Thread

from utils import colorprint
from better_way_55_1 import (
    step1_download,
    step2_resize,
    step3_upload
)


class BetterQueue(Queue):
    SENTINEL = object()

    def close(self):
        self.put(self.SENTINEL)

    def __iter__(self):
        while True:
            item = self.get()
            try:
                if item is self.SENTINEL:
                    return
                yield item
            finally:
                self.task_done()


class StoppableWorker(Thread):
    def __init__(self, func, in_queue, out_queue):
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue

    def run(self):
        # `self.in_queue` 는 앞서 구현한 이터레이터 프로토콜을 따른다.
        # 이터레이터 프로토콜은 파이썬의 for 루프나 이와 연관된 식이
        # 컨테이너 타입의 내용을 방문할 때 사용하는 절차다.
        # 이것은 실제로 `iter(self.in_queue)` 를 호출한다.
        # `iter()` 은 `self.in_queue.__iter__` 을 호출한다.
        # 이터레이터가 소진될 때까지 실행된다.
        for item in self.in_queue:
            result = self.func(item)
            self.out_queue.put(result)
            # 뒷쪽 큐의 최대 사이즈보다 더 많은 데이터를 삽입하는 경우에 대한 처리를
            # `put` 메서드가 알아서 처리해 주기 때문에 편하다!


def start_threads(count, *args):
    # 이제부터는 하나의 큐를 여러 개의 스레드가 처리하는 것도 쉽게 가능하다.
    threads = [StoppableWorker(*args) for _ in range(count)]
    for thread in threads:
        thread.start()
    return threads


def stop_threads(queue: BetterQueue, threads: list[Thread]):
    for _ in threads:
        queue.close()
    queue.join()

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    # 파이프라인 중간이 막히는 경우를 대비하여 Queue 클래스에서는
    # 파이프라인 사이에 놓인 큐에 들어갈 수 있는 미완성 작업의 최대 개수를 지정할 수 있다.
    # 큐 원소가 소비되지 않으면 더이상 값을 추가하지 못하도록 막고 대기한다.
    # 예를 들어 1000개로 제한해 보자.
    download_queue = BetterQueue(1000)
    resize_queue = BetterQueue(1000)
    upload_queue = BetterQueue(1000)
    done_queue = BetterQueue()

    download_threads = start_threads(
        1, step1_download, download_queue, resize_queue)
    resize_threads = start_threads(
        1, step2_resize, resize_queue, upload_queue)
    upload_threads = start_threads(
        1, step3_upload, upload_queue, done_queue)

    colorprint('큐에 데이터 입력, 시간 측정 시작')
    t_start = time.time()

    for _ in range(1000):
        download_queue.put(object())

    stop_threads(download_queue, download_threads)
    stop_threads(resize_queue, resize_threads)
    stop_threads(upload_queue, upload_threads)

    t_end = time.time()
    colorprint('모든 스레드들의 조인 완료, 시간 측정 끝')

    print(f'{done_queue.qsize()} 개의 원소가 처리되었습니다.')
    print(f'총 처리 시간은 {t_end-t_start:3f}초 입니다.')

# 실제로 이 경우 `better_way_55_1.py` 보다 거의 7~8배 나은 성능을 보여준다.
# 만약 `start_threads` 의 첫 번째 인자의 크기를 키워 블로킹 IO를 처리하는 스레드의 수를 늘린다면
# 프로그램의 속도가 매우 빨라지는 것을 확인할 수 있다.
# 각각의 큐에 쓰레드를 10개씩 붙여주는 경우, `better_way_55_1.py` 보다 약 90배 빠르다.
