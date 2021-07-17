import time
from threading import Thread


def main():
    t = Thread(target=func)  # 创建线程
    t.start()  # 多线程可以开始执行了


def func():
    for i in range(0, 100):
        print('func' + str(i))


class MyThread(Thread):
    def __init__(self, nums):
        super().__init__()
        self.nums = nums

    def run(self):
        for i in range(0, 10):
            print(f"子线程{i}")
            time.sleep(1)


if __name__ == '__main__':
    # t = Thread(target=func)  # 创建线程
    # t.start()  # 多线程可以开始执行了
    # for i in range(0, 100):
    #     print("|main:" + str(i))
    t = MyThread()
    t.start()
    for i in range(0, 10):
        print(f"主线程{i}")
        time.sleep(1)
