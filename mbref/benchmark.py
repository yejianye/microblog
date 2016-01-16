#!/usr/bin/env python
"""Benchmark performance for microblog
"""
import argparse
import time
import random
import logging.config
from threading import Thread
from Queue import Queue, Empty

from mbref.client import Client

class Executor(Thread):
    def __init__(self, client, jobs):
        super(Executor, self).__init__()
        self.client = client
        self.jobs = jobs

    def run(self):
        while True:
            try:
                job = self.jobs.get_nowait()
                cmd = getattr(self.client, job['cmd'])
                cmd(*job['args'], **job['kwargs'])
            except Empty:
                break

def _monitor(jobs):
    while jobs.qsize() > 0:
        logging.info('%d jobs left...', jobs.qsize())
        time.sleep(1)

def _execute(client, jobs, thread_count):
    logging.info('Start executing requests...')
    start_time = time.time()
    job_count = jobs.qsize()
    workers = [Executor(client, jobs) for _ in xrange(thread_count)]
    monitor = Thread(target=_monitor, args=(jobs,))
    monitor.daemon = True
    monitor.start()
    [t.start() for t in workers]
    [t.join() for t in workers]
    logging.info('All requests are completed.')
    return {
        'job_count': job_count,
        'time':time.time() - start_time
    }

def _add_job(jobs, cmd, *args, **kwargs):
    jobs.append({
        'cmd': cmd,
        'args': args,
        'kwargs': kwargs
        })

def _list2queue(l):
    q = Queue()
    [q.put(i) for i in l]
    return q

def write_test(client, thread_count, test_size):
    client.clear_all()
    base_count = {
        'small': 100,
        'medium': 1000,
        'large': 10000,
    }[test_size]

    jobs = []
    # Reference time: 2016/01/14 6:45PM
    ref_ts = 1452768307

    # create a bunch of users
    logging.info('Generate create_user requests...')
    for i in xrange(base_count):
        _add_job(jobs, 'create_user',
                 username = 'user{}'.format(i),
                 email = 'user{}@example.com'.format(i),
                 password = 'secret',
                 bio = "I'm user {}".format(i))

    # for each user post 3-5 feeds
    logging.info('Generate post_feed requests...')
    for uid in xrange(1, base_count+1):
        [_add_job(jobs, 'post_feed',
                 user_id = uid,
                 content = "My favorite number is {}".format(random.randint(1, 9)),
                 time_created = ref_ts - random.randint(0, base_count * 10)
                 ) for _ in xrange(random.randint(3,5))]
    logging.info('Generate create_user requests...')

    # each user follow 1 - 3 users
    logging.info('Generate follow requests...')
    for uid in xrange(1, base_count+1):
        [_add_job(jobs, 'follow',
                  user_id = uid,
                  other_id = random.randint(1, base_count+1)
                  ) for _ in xrange(random.randint(1,3))]
    return _execute(client, _list2queue(jobs), thread_count)

def read_test(client, thread_count, test_size):
    base_count = {
        'small': 30,
        'medium': 300,
        'large': 3000,
    }[test_size]
    jobs = []
    _repeat = lambda: xrange(random.randint(1, 10))
    logging.info('Generate get_user requests...')
    for uid in xrange(1, base_count+1):
        [_add_job(jobs, 'get_user', uid) for _ in _repeat()]

    logging.info('Generate get_user_feeds and get_friend_feeds requests...')
    for uid in xrange(1, base_count+1):
        [_add_job(jobs, 'get_user_feeds', uid) for _ in _repeat()]
        [_add_job(jobs, 'get_friend_feeds', uid) for _ in _repeat()]

    logging.info('Generate get follower/following requests...')
    for uid in xrange(1, base_count+1):
        [_add_job(jobs, 'get_followers', uid) for _ in _repeat()]
        [_add_job(jobs, 'get_followings', uid) for _ in _repeat()]
    random.shuffle(jobs)
    return _execute(client, _list2queue(jobs), thread_count)

def init_logger():
    log_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '[%(asctime)s] [%(levelname)s] %(message)s'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'level': 'INFO',
            }
        },
        'loggers': {
            '': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': True
            },
            'requests': {
                'handlers': ['console'],
                'level': 'WARN',
                'propagate': True
            },
        }
    }
    logging.config.dictConfig(log_config)

def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--write-test", action='store_true',
                        default=False, help="Perform benchmark for write test")
    parser.add_argument("--read-test", action='store_true',
                        default=False, help="Perform benchmark for read test")
    parser.add_argument("--concurrency", type=int, default=10,
                        help="Number of concurrent client sending requests")
    parser.add_argument("--test-size", default='medium',
                        help="Size of the benchmark test (small/medium/large)")
    parser.add_argument("--api-url", default='http://localhost:7431',
                        help="Base URL for microblog API")
    args = parser.parse_args()
    init_logger()
    client = Client(args.api_url)
    if args.write_test:
        perf = write_test(client, args.concurrency, args.test_size)
        print 'Write test result:'
        print 'Completed {job_count} requests in {time} seconds'.format(**perf)
        print 'Avg req/sec: {}\n'.format(perf['job_count'] / perf['time'])
    if args.read_test:
        perf = read_test(client, args.concurrency, args.test_size)
        print 'Read test result:'
        print 'Completed {job_count} requests in {time} seconds'.format(**perf)
        print 'Avg req/sec: {}\n'.format(perf['job_count'] / perf['time'])

if __name__ == '__main__':
    main()

