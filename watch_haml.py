#!/usr/bin/env python
#
# Usage:
#   ./watch_haml.py
#
# Watches current directory and, if filename.haml is modified, runs
#
# haml filename.haml filename.html
#
# based on autocompile.py example from
# https://github.com/seb-m/pyinotify/
#
# requires pyinotify

import subprocess
import sys
import pyinotify


class OnWriteHandler(pyinotify.ProcessEvent):
    def process_IN_MODIFY(self, event):
        pathname = event.pathname
        if not pathname.endswith('haml'):
            return
        print pathname
        cmd = 'haml %s %s.html' % (pathname, pathname[:-5])
        subprocess.call(cmd.split(' '))


def auto_haml_to_html():
    path = '.'
    wm = pyinotify.WatchManager()
    handler = OnWriteHandler()
    notifier = pyinotify.Notifier(wm, default_proc_fun=handler)
    wm.add_watch(path, pyinotify.ALL_EVENTS, rec=True, auto_add=True)
    print '==> Start monitoring %s (type c^c to exit)' % path
    notifier.loop()

if __name__ == '__main__':
    auto_haml_to_html()
