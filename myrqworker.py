#!/usr/bin/env python
import sys
from rq import Queue, Connection, Worker

# Preload libraries
import web.app
from web.util import _redis

import jieba.analyse # import this to load dict

# Provide queue names to listen to as arguments to this script,
# similar to rqworker
with Connection(connection=_redis):
    qs = map(Queue, sys.argv[1:]) or [Queue()]

    w = Worker(qs)
    w.work()
