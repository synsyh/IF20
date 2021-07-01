"""
IF20-test_thread by Yuning Sun
1:11 PM 7/1/21
Module documentation: 
"""
import threading
import time


class Shared:
    def __init__(self):
        self.value = 0

    def set(self, value):
        self.value = value

    def get(self):
        return self.value


class MyThread(threading.Thread):
    def __init__(self, thread_id, shared):
        super().__init__()
        self.thread_id = thread_id
        self.shared = shared

    def run(self) -> None:
        i = 10
        while i > 0:
            time.sleep(1)
            self.shared.set(self.shared.get() + 10)
            i -= 1


class Monitor(threading.Thread):
    def __init__(self, shared):
        super().__init__()
        self.shared = shared

    def run(self) -> None:
        while True:
            time.sleep(0.5)
            print(self.shared.get())


def main():
    shared = Shared()
    my_thread = MyThread("dudulu", shared)
    monitor = Monitor(shared)
    my_thread.start()
    monitor.start()
    my_thread.join()
    monitor.join()


if __name__ == '__main__':
    main()
