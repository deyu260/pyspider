#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Binux<i@binux.me>
#         http://binux.me
# Created on 2014-03-05 00:11:49

import sys
import time
import logging
import logging.config
from multiprocessing import Queue
from database.sqlite import taskdb, projectdb
from libs.utils import run_in_thread, run_in_subprocess

logging.config.fileConfig("logging.conf")

def get_taskdb():
    return taskdb.TaskDB('./data/task.db')

def get_projectdb():
    return projectdb.ProjectDB('./data/project.db')

queue_maxsize = 100
newtask_queue = Queue(queue_maxsize)
status_queue = Queue(queue_maxsize)
scheduler2fetcher = Queue(queue_maxsize)
fetcher2processor = Queue(queue_maxsize)

scheduler_xmlrpc_port = 23333
fetcher_xmlrpc_port = 24444
debug = True

def run_scheduler():
    from scheduler import Scheduler
    scheduler = Scheduler(taskdb=get_taskdb(), projectdb=get_projectdb(),
            newtask_queue=newtask_queue, status_queue=status_queue, out_queue=scheduler2fetcher)

    run_in_thread(scheduler.xmlrpc_run, port=scheduler_xmlrpc_port)
    scheduler.run()

def run_fetcher():
    from fetcher.tornado_fetcher import Fetcher
    fetcher = Fetcher(inqueue=scheduler2fetcher, outqueue=fetcher2processor)

    run_in_thread(fetcher.xmlrpc_run, port=fetcher_xmlrpc_port)
    fetcher.run()

def run_processor():
    from processor import Processor
    processor = Processor(projectdb=get_projectdb(),
            inqueue=fetcher2processor, status_queue=status_queue, newtask_queue=newtask_queue)
    
    processor.run()

def run_webui():
    import xmlrpclib
    import cPickle as pickle
    scheduler_rpc = xmlrpclib.ServerProxy('http://localhost:%d' % scheduler_xmlrpc_port)
    fetch_rpc = xmlrpclib.ServerProxy('http://localhost:%d' % fetcher_xmlrpc_port)

    from webui.app import app
    app.config['fetch'] = lambda task: pickle.loads(fetch_rpc.fetch(task).data)
    app.config['projectdb'] = get_projectdb
    app.config['scheduler_rpc'] = scheduler_rpc
    #app.config['cdn'] = '//cdnjs.cloudflare.com/ajax/libs/'
    app.run('0.0.0.0')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        threads = []
        threads.append(run_in_subprocess(run_fetcher))
        threads.append(run_in_subprocess(run_processor))
        threads.append(run_in_subprocess(run_scheduler))
        threads.append(run_in_subprocess(run_webui))

        while True:
            try:
                time.sleep(10)
            except KeyboardInterrupt:
                break

        for each in threads:
            each.join()
    else:
        cmd = "run_"+sys.argv[1]
        locals()[cmd]()
