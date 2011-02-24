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
import os
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

def check_that_html_exist():
    ignore = ['.git','.hg']
    for root, dirs, files in os.walk('.'):
        if all(not ig in root for ig in ignore):
            print root
            for file in files:
                if file.endswith('.haml'):
                    src = os.path.join(root, file)
                    dst = os.path.join(root, file[:-5]+".html")
                    if not os.path.exists(dst):
                        print dst
                        print "does not exist"
                        cmd = 'haml %s %s' % (src, dst)
                        subprocess.call(cmd.split(' '))

if __name__ == '__main__':
    check_that_html_exist()
    auto_haml_to_html()
