# -*- coding: utf-8 -*-

# http request pool
# Created: 2016-07-20
# Copyright: (c) 2016<smileboywtu@gmail.com>


import gevent
import gevent.monkey
from gevent.lock import RLock
from gevent.queue import Queue
gevent.monkey.patch_all()


class HttpPool(object):
    """http request pool"""

    def __init__(self, load, runner=None):
        """

        :param load: default http request load
        """
        self.runner = runner
        self.jobs = []
        self.max_requst = load
        self.lock = RLock()
        self.task_queue = Queue()

    @property
    def runner(self):
        return self.runner

    @runner.setter
    def set_runner(self, runner):
        """

        :return: None
        """
        self.runner = runner

    def add_task(self, task):
        """
        add a single task to the queue

        :param task: a http requst task
        :return:
        """
        self.task_queue.put(task)

    def add_tasks(self, tasks):
        """
        add multiple task to the queue

        :param tasks: list of the tasks
        :return: None
        """
        for task in xrange(tasks):
            self.add_task(task)

    def run(self):
        """
        start to run the jobs

        :return: None
        """
        if not self.runner:
            raise ValueError("please setup runner first.")

        while not Queue.empty():
            with self.lock:
                if self.max_requst > 0:
                    job = gevent.spawn(self.runner, self.task_queue.get())
                    self.jobs.append(job)
                    self.max_requst -= 1
                else:
                    gevent.joinall(self.jobs)
            gevent.sleep(0.001)
