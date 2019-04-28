import asyncio
from collections import deque


def done_callback(future):
    future._loop.stop()


class Loop:
    def __init__(self):
        self._ready = deque()
        self._stopping = False

    def create_task(self, coro):
        task = asyncio.tasks.Task(coro, loop=self)
        return task

    def run_until_complete(self, future):
        # 获取任务
        future = asyncio.tasks.ensure_future(future, loop=self)
        # 增加任务到self._ready
        future.add_done_callback(done_callback)
        # 跑全部任务
        self.run_forever()
        # 从self._ready中移除
        future.remove_done_callback(done_callback)

    def run_forever(self):
        try:
            while 1:
                self._run_once()
                if self._stopping:
                    break
        finally:
            self._stopping = False

    def call_soon(self, cb, *args):
        self._ready.append((cb, args))

    def _run_once(self):
        ntodo = len(self._ready)
        for i in range(ntodo):
            t, a = self._ready.popleft()
            t(*a)

    def stop(self):
        self._stopping = True

    def close(self):
        self._ready.clear()

    def get_debug(self):
        return False


async def foo():
    print("Hello Foo")


async def bar():
    print("Hello Bar")


loop = Loop()
tasks = [loop.create_task(foo()), loop.create_task(bar())]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
