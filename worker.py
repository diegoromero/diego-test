import os

import redis
from rq import Worker, Queue, Connection
import urlparse

listen = ['high', 'default', 'low']

redis_url = urlparse.urlparse(os.environ.get('REDISCLOUD_URL'))

conn = redis.Redis(host=redis_url.hostname, port=redis_url.port, db=0, password=redis_url.password)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()
