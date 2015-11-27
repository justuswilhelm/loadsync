from asyncio import get_event_loop, wait
from logging import basicConfig
from time import time

from aiohttp import get


async def client_request(url):
    start = time()
    response = await get(url)
    await response.text()
    duration = time() - start
    return duration


def main():
    def gen_tasks():
        for _ in range(requests):
            yield client_request(url)
    url = "http://www.twogifs.com"
    requests = 90
    print("Requesting {} {} times".format(url, requests))
    tasks = list(gen_tasks())
    loop = get_event_loop()
    start = time()
    done, _ = loop.run_until_complete(wait(tasks))
    average_task_duration = sum(
        map(lambda task: task.result(), done)) / requests
    duration = time() - start
    print("Duration: {} seconds".format(duration))
    print("Average task duration: {} seconds".format(average_task_duration))


if __name__ == "__main__":
    basicConfig(level='DEBUG')
    main()
