#!/usr/bin/env python

import sys
import os.path
import logging

from subprocess import call, check_call, check_output

log_dir = "/www/mirrors/log/"
mirror_dir = "/www/mirrors"


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
    logger.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    return logger


def du_size(mirror):
    mirror_path = os.path.join(mirror_dir, mirror)
    r = check_output(["du", "-s", mirror_path])
    return r.split("\n")[0].split("\t")[0]

 
def get_size(stage):
    pypi_mirror = "pypi"
    pypi_log = os.path.join(log_dir, "pypi.log")
    if stage == "start":
        with open(pypi_log, 'r') as log:
            lines = log.readlines()
            if lines.__len__() == 0:
                return du_size(pypi_mirror)
            last_size = lines[-1].split()[-1]
            return last_size
    elif stage == "end":
        with open(pypi_log, 'r') as log:
            lines = log.readlines()
	    last_code = lines[-1].split()[-1]
            if last_code == '0':
	         return du_size(pypi_mirror)
            return lines[-2].split()[-1]
    return '0'
            

def dry_run():
    pypi_logger = setup_pypi_logging()
    pypi_logger.info(" - ".join(["SyncStart", get_size("start")]))
    for i in range(5):          # Try five times
        rc = check_call(["bandersnatch/bin/bandersnatch",
                         "-c", "bandersnatch/bandersnatch.conf", "mirror"])
        if rc == 0:
            pypi_logger.info(" - ".join(["SyncSuccd", str(rc)]))
            break
        elif i == 4:    
            pypi_logger.info(" - ".join(["SyncError", str(rc)]))
    pypi_logger.info(" - ".join(["SyncCompt", get_size("end")]))


def report():
    call(["bandersnatch/bin/bandersnatch", 
          "-c", "bandersnatch/bandersnatch.conf", "update-stats", 
          "|&", "logger", "-t", "bandersnatch[update-stats]"])


def run_with_verbose():
    call(["bandersnatch/bin/bandersnatch",
          "-c", "bandersnatch/bandersnatch-debug.conf",
          "mirror"])


def main(argv):
    if argv.__len__() == 0:
        dry_run()
    elif argv.__len__() == 1 and argv[0] == "-v":
        run_with_verbose()
    elif argv.__len__() == 1 and argv[0] == "-u":
        pass
	# report()
    else:
        print "usage: python pypi.py [-v|-u]"


def test():
    get_size("end")


if __name__ == "__main__":
    main(sys.argv[1:])
