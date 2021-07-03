"""
IF20-test_thread by Yuning Sun
1:11 PM 7/1/21
Module documentation: 
"""
import threading
import time


class Shared:
    def __init__(self):
        self._value = 0

    def set(self, value):
        self._value = value

    def get(self):
        return self._value


class MyThread(threading.Thread):
    def __init__(self, thread_id, shared):
        super().__init__()
        self.thread_id = thread_id
        self.shared = shared
        self.flag = True

    def stop(self):
        self.flag = False

    def run(self) -> None:
        while self.flag:
            time.sleep(1)
            self.shared.set(self.shared.get() + 10)


class Monitor(threading.Thread):
    def __init__(self, shared, monitor):
        super().__init__()
        self.shared = shared
        self.monitor = monitor

    def run(self) -> None:
        i = 10
        while i > 0:
            time.sleep(0.5)
            print(self.shared.get())
            i -= 1
        self.monitor.stop()


def main():
    shared = Shared()
    my_thread = MyThread("dudulu", shared)
    monitor = Monitor(shared, my_thread)
    my_thread.start()
    monitor.start()
    my_thread.join()
    monitor.join()


if __name__ == '__main__':
    main()
