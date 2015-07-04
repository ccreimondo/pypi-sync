#!/usr/bin/env python

import sys
import os.path
import logging

from subprocess import call, check_call

log_dir = "/www/mirrors/log/"


def setup_pypi_logging():
    """Logging for front-end to get sync state

    Returns:
        logger: logging instance
    """
    pypi_log_file = os.path.join(log_dir, "pypi.log")
    fh = logging.FileHandler(pypi_log_file)
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter(fmt="%(asctime)s - %(message)s",
                                  datefmt="%Y%m%d - %H:%M:%S")
    fh.setFormatter(formatter)

    logger = logging.getLogger("pypi")
    logger.addHandler(fh)
    return logger


def dry_run():
    pypi_logger = setup_pypi_logging()

    pypi_logger.info("SyncStart")
    for i in range(5):          # Try five times
        rc = check_call("bandersnatch/bin/bandersnatch",
                        "-c", "bandersnatch/bandersnatch.conf")
        if rc == 0:
            pypi_logger.info("SyncSuccd - 0")
            break
        elif i == 4:    
            pypi_logger.info("SyncError - 1")
    pypi_logger.info("SyncCompt")


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
