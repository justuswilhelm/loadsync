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
        async with get(url) as response:
            await response.text()
    duration = time() - start
    return duration


def gen_progress_bar(tasks, loop):
    print("In Progress")
    loop.call_soon(progress_bar, tasks, loop)
    print("")


def progress_bar(requests, loop, freq=0.01):
    width, _ = get_terminal_size()
    done_count = len(tuple(filter(lambda t: t.done(), Task.all_tasks())))
    tasks_left_count = requests - done_count
    progress = int(done_count / requests * width)
    print("\r" + "*" * progress + "." * (width - progress), end="")
    if tasks_left_count > 0:
        loop.call_later(freq, progress_bar, requests, loop)


def run(tasks, loop):
    start = time()
    done, _ = loop.run_until_complete(tasks)
    duration = time() - start
    return done, duration


def main():
    def gen_tasks():
        for _ in range(requests):
            yield client_request(url)

    # FIXME argparse!
    url = argv[1]
    requests = int(argv[2])
    print("Requesting {} {} times".format(url, requests))
    tasks = wait(list(gen_tasks()))
    loop = get_event_loop()
    gen_progress_bar(requests, loop)
    done, duration = run(tasks, loop)
    average_task_duration = sum(
        map(lambda task: task.result(), done)) / requests
    print("Duration: {} seconds".format(duration))
    print("Average task duration: {} seconds".format(average_task_duration))


if __name__ == "__main__":
    basicConfig(level='DEBUG')
    main()
