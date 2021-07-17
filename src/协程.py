import asyncio
import time


async def fun1():
    print("func1")
    await asyncio.sleep(3)
    print("fun1")
    return 'fun1--result'


async def fun2():
    print("func2")
    await asyncio.sleep(2)
    print("fun2")
    return 'fun2--result'


async def fun3():
    print("func3")
    await asyncio.sleep(1)
    print("fun3")
    return 'fun3--result'


async def main():
    task = [
        asyncio.create_task(fun1()),
        asyncio.create_task(fun2()),
        asyncio.create_task(fun3())
    ]
    await asyncio.wait(task)


if __name__ == '__main__':
    start = time.time()
    loop = asyncio.get_event_loop()
    # task1 = loop.create_task(fun1())
    # task2 = loop.create_task(fun2())
    # task3 = loop.create_task(fun3())
    loop.run_until_complete(main())
    # asyncio.run(main())
    # asyncio.run(asyncio.wait([fun1(), fun2(), fun3()])) # 同时执行多个任务
    end = time.time()
    print(end - start)
