#!/usr/bin/env python

import sys
import os.path
import logging

from subprocess import call, check_call, check_output

MIRROR_NAME = "pypi"
MIRROR_DIR = "/www/mirrors"
BIN_DIR = os.path.join(MIRROR_DIR, "bin")
LOG_DIR = os.path.join(MIRROR_DIR, "log")
BANDERSNATCH_ENV = os.path.join(BIN_DIR, "bandersnatch")
BANDERSNATCH_BIN = os.path.join(BANDERSNATCH_ENV, "bin/bandersnatch")
BS_CONF = os.path.join(BANDERSNATCH_ENV, "bandersnatch.conf")
BS_DEBUG_CONF = os.path.join(BANDERSNATCH_ENV, "bandersnatch-debug.conf")

def setup_logging():
    """Logging for front-end to get sync state

    Returns:
        logger: logging instance
    """
    log_file = os.path.join(LOG_DIR, ''.join([MIRROR_NAME, ".log"]))

    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter(fmt="%(asctime)s - %(message)s",
                                  datefmt="%Y%m%d - %H:%M:%S")
    fh.setFormatter(formatter)

    logger = logging.getLogger(MIRROR_DIR)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    return logger


def du_size(mirror):
    mirror_path = os.path.join(MIRROR_DIR, mirror)
    r = check_output(["du", "-s", mirror_path])
    return r.split("\n")[0].split("\t")[0]

 
def get_size(stage):
    log_file = os.path.join(LOG_DIR, ''.join([MIRROR_NAME, ".log"]))

    if stage == "start":
        with open(log_file, 'r') as log:
            lines = log.readlines()
            if lines.__len__() == 0:
                return du_size(MIRROR_NAME)
            last_size = lines[-1].split()[-1]
            return last_size
    elif stage == "end":
        with open(log_file, 'r') as log:
            lines = log.readlines()
	    last_code = lines[-1].split()[-1]
            if last_code == '0':
	            return du_size(MIRROR_NAME)
            return lines[-2].split()[-1]
    return '0'
            

def dry_run():
    logger = setup_logging()
    logger.info(" - ".join(["SyncStart", get_size("start")]))
    for i in range(5):          # Try five times
        rc = check_call([BANDERSNATCH_BIN, "-c", BS_CONF, "mirror"])
        if rc == 0:
            logger.info(" - ".join(["SyncSuccd", str(rc)]))
            break
        elif i == 4:    
            logger.info(" - ".join(["SyncError", str(rc)]))
    logger.info(" - ".join(["SyncCompt", get_size("end")]))


def report():
    # TODO
    call([BANDERSNATCH_BIN, "-c", BS_CONF, "update-stats", 
          "|&", "logger", "-t", "bandersnatch[update-stats]"])


def run_with_verbose():
    call([BANDERSNATCH_BIN, "-c", BS_DEBUG_CONF, "mirror"])


def main(argv):
    if argv.__len__() == 0:
        dry_run()
    elif argv.__len__() == 1 and argv[0] == "-v":
        run_with_verbose()
    elif argv.__len__() == 1 and argv[0] == "-u":
        pass
	# report()
    else:
        usage_msg = ' '.join(["usage:", "python", __file__, "[-v|-u]"])
        print usage_msg


def test():
    get_size("end")


if __name__ == "__main__":
    main(sys.argv[1:])
