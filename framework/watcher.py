# -*- coding: utf-8 -*-
# @Time    : 2017/6/29 10:07
# @Author  : baiyoudong
# @File    : watcher.py
import os
import sys


class Watcher:
    def __init__(self):
        self.child = os.fork()
        if self.child == 0:
            return
        else:
            self.watch()

    def watch(self):
        try:
            os.wait()
        except KeyboardInterrupt:
            print 'KeyboardInterrupt'
            self.kill()
        finally:
            sys.exit()

    def kill(self):
        import signal
        try:
            os.kill(self.child, signal.SIGKILL)
        except OSError:
            pass
