from asyncio import (
    get_event_loop,
    wait,
    Semaphore,
    Task,
)
from os import get_terminal_size
from logging import basicConfig
from sys import argv
from time import time

from aiohttp import get

MAX_CONCURRENT = 5
request_semaphore = Semaphore(MAX_CONCURRENT)


async def client_request(url):
    start = time()
    async with request_semaphore:
        response = await get(url)
        await response.text()
    duration = time() - start
    return duration


def main():
    def gen_tasks():
        for _ in range(requests):
            yield client_request(url)

    def progress_bar(freq=0.01):
        width, _ = get_terminal_size()
        running = int(
            len(tuple(filter(lambda t: t.done(), Task.all_tasks()))) /
            requests * width)
        print("\r" + "*" * running + "." * (width - running), end="")
        loop.call_later(freq, progress_bar)

    # FIXME argparse!
    url = argv[1]
    requests = int(argv[2])
    print("Requesting {} {} times".format(url, requests))
    tasks = list(gen_tasks())
    loop = get_event_loop()
    start = time()
    print("In Progress")
    loop.call_soon(progress_bar)
    print("")
    done, _ = loop.run_until_complete(wait(tasks))
    average_task_duration = sum(
        map(lambda task: task.result(), done)) / requests
    duration = time() - start
    print("Duration: {} seconds".format(duration))
    print("Average task duration: {} seconds".format(average_task_duration))


if __name__ == "__main__":
    basicConfig(level='DEBUG')
    main()
