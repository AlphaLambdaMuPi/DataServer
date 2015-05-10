#!/usr/bin/env python

import asyncio
import logging
import subprocess

from server import data_server
import logsetting
from settings import settings as SETTINGS

logsetting.log_setup()
logger = logging.getLogger()

@asyncio.coroutine
def check_tasks():
    now = len(asyncio.Task.all_tasks())
    while now > 2:
        yield from asyncio.sleep(1)
        # print(asyncio.Task.all_tasks())
        now = len(asyncio.Task.all_tasks())


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    coro = asyncio.start_server(data_server, SETTINGS['ip'], SETTINGS['port'])
    s = loop.run_until_complete(coro)

    logger.info('serving on {}'.format(s.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print()
        loop.run_until_complete(data_server.stop())
    finally:
        loop.run_until_complete(check_tasks())
        loop.close()
        print("exit.")

