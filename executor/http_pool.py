# -*- coding: utf-8 -*-

# http request pool
# Created: 2016-07-20
# Copyright: (c) 2016<smileboywtu@gmail.com>


import gevent
import gevent.monkey
from gevent import Greenlet
from gevent.lock import RLock
from gevent.queue import Queue
gevent.monkey.patch_all()


class HttpPool(object):
    """http request pool"""

    def __init__(self, load, runner=None):
        """

        :param load: default http request load
        """
        self._runner = runner
        self.jobs = []
        self.jobs_ = []
        self.result = []
        self.max_requst = load
        self.lock = RLock()     # 控制写入job_
        self.lock_ = RLock()    # 控制输出结果
        self.task_queue = Queue()

    @property
    def runner(self):
        return self._runner

    @runner.setter
    def set_runner(self, runner):
        """

        :return: None
        """
        self._runner = runner

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
        for task in tasks:
            self.add_task(task)

    def _callback(self, job):
        """

        :return: None
        """
        # 获取结果
        with self.lock_:
            value = job.value
            if isinstance(value, list):
                self.result.extend(value)
            else:
                self.result.append(value)

        if not self.task_queue.empty():
            job = gevent.spawn(self.runner, self.task_queue.get())
            job.link(self._callback)
            with self.lock:
                self.jobs_.append(job)

    def run(self):
        """
        start to run the jobs

        :return: return jobs
        """
        if not self.runner:
            raise ValueError("please setup runner first.")

        http_load = self.max_requst
        while not self.task_queue.empty():
            if http_load > 0:
                job = gevent.spawn(self.runner, self.task_queue.get())
                job.link(self._callback)
                self.jobs.append(job)
                http_load -= 1
            else:
                gevent.joinall(self.jobs)

        if http_load > 0:
            gevent.joinall(self.jobs)

        with self.lock:
            gevent.joinall(self.jobs_)

        return self.result
