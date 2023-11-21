""" 동시성(concurrency)은 컴퓨터가 같은 시간에 여러 작업을 처리하는 것,
병렬성(parallelism)은 같은 시간에 여러 작업을 '실제로' 처리하는 것이다.
파이썬에서는 동시성을 위해 `Thread`를, 병렬성은 `subprocess`를 이용하는 것이 가장 일반적이다.
`os.popen`, `os.exec` 와 같은 하위 프로세스 실행 방법들보다 `subprocess` 모듈이 낫다.
`subprocess` 모듈의 `run` 함수를 실행해도 되고, `Popen` 클래스를 사용해도 좋다.
프로세스 간 데이터는 PIPE를 이용해 연결할 수 있다.
"""
