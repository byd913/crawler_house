# -*- coding: utf-8 -*-
# @Time    : 2017/6/27 09:48
# @Author  : baiyoudong
# @File    : rw_lock.py

import threading


class RWLock:
    def __init__(self):
        self.r_lock = threading.Lock()
        self.w_lock = threading.Lock()
        self.reader = 0

    def write_acquire(self):
        self.w_lock.acquire()

    def write_release(self):
        self.w_lock.release()

    def read_acquire(self):
        self.r_lock.acquire()
        self.reader += 1
        if self.reader == 1:
            self.w_lock.acquire()
        self.r_lock.release()

    def read_release(self):
        self.r_lock.acquire()
        self.reader -= 1
        if self.reader == 0:
            self.w_lock.release()
        self.r_lock.release()
