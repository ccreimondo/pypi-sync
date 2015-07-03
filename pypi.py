#!/usr/bin/env python

import sys.argv
import os.path

from subprocess import call, check_call

def active_log_conf():
    if os.path.isfile("bandersnatch/bandersnatch-log.conf"):
        return

    if os.path.isfile("bandersnatch-log.conf"):
        rc = check_call(["mv", "bandersnatch-log.conf", "bandersnatch/"])
    else:
        # TODO Create default log file
        pass


def active_bandersnatch_conf():
    if os.path.isfile("bandersnatch/bandersnatch.conf"):
        return
    # TODO Create bandersnatch.conf
    pass


def dry_run():
    """Ban console log with the help of advance log configure file"""
    active_log_conf()
    active_bandersnatch_conf()
    for i in range(5):          # Try five times
        rc = check_call("bandersnatch/bin/bandersnatch", "-c", "bandersnatch/bandersnatch.conf")


def run_with_verbose():
    call(["bandersnatch/bin/bandersnatch",
          "-c", "bandersnatch/bandersnatch-debug.conf",
          "mirror"])


def main(argv):
    if argv.__len__() == 1:
        dry_run()
    elif argv.__len__() == 2 and argv[1] == "-v":
        run_with_verbose()
    else:
        print "usage: python pypi.py [-v]"


if __name__ == "__main__":
    main(sys.argv[1:0])
