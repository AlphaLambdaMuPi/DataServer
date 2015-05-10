#! /usr/bin/env python

import asyncio
import logging
import uuid
import hashlib
import hmac
import json
from collections import defaultdict

from connection import JsonConnection

logger = logging.getLogger()

class DataServer:
    def __init__(self, loop=None):
        self._loop = loop
        if not self._loop:
            self._loop = asyncio.get_event_loop()
        self._datas = defaultdict(list)
        self._conns = {}

    @asyncio.coroutine
    def __call__(self, sr, sw):
        conn = JsonConnection(sr, sw)
        data = yield from conn.recv()
        if not isinstance(data, dict):
            return
        if 'name' in data and isinstance(data['name'], str):
            if data['name'] in self._conns:
                logger.warning('same device connection!')
                return
            self._conns[data['name']] = conn
            record = []
            self._datas[data['name']].append(record)
            yield from self.record_data(conn, data['name'], record)
    
    @asyncio.coroutine
    def record_data(self, conn, name, record):
        while True:
            data = yield from conn.recv()
            if not isinstance(data, dict):
                continue
            if 'stop' not in data and len(record) < 5000:
                record.append(data)
            else:
                logger.debug('data count: {}'.format(len(record)))
                recordpath = 'data/{}-{}.txt'.format(
                    name,
                    len(self._datas[name])
                )
                with open(recordpath, 'w') as f:
                    for r in record:
                        print(json.dumps(r), file=f)
                self._conns[name].close()
                del self._conns[name]
                break

    @asyncio.coroutine
    def stop(self):
        for conn in self._conns.values():
            yield from conn.close()

# global object       
data_server = DataServer() 

