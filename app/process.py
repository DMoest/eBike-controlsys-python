#!/usr/bin/env python3

from multiprocessing import Process

class WorkerProcess():
    """
    Wrapper around multiporcessing.Process.
    """
    _job = None
    _process = None

    def __init__(self, job):
        self._job = job
        self._process = Process(target=job)

    def start(self):
        self._process.start()

    def terminate(self):
        self._process.terminate()
        self._process.join()
