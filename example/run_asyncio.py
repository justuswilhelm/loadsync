from asyncio import get_event_loop, sleep
from datetime import datetime

from aiohttp import web

async def handle(request):
    print("GET /large.csv HTTP/1.1 200")
    response = web.StreamResponse()
    await response.prepare(request)
    for i in range(10):
        await sleep(0.1)
        response.write((datetime.now().isoformat() + '\n').encode())
        await response.drain()
    await response.write_eof()
    return response

async def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/large.csv', handle)

    srv = await loop.create_server(
        app.make_handler(), '127.0.0.1', 6000)
    print("Server started at http://127.0.0.1:6000")
    return srv

loop = get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()
