#!/usr/bin/env python

import os.path

from ConfigParser import SafeConfigParser
from subprocess import call

MIRROR_DIR = "/www/mirrors/"
BIN_DIR = os.path.join(MIRROR_DIR, "bin")
LOG_DIR = os.path.join(MIRROR_DIR, "log")
BANDERSNATCH_ENV_DIR = os.path.join(BIN_DIR, "bandersnatch")
CONF_FILE_PREFIX = os.path.join(BANDERSNATCH_ENV_DIR, "bandersnatch")
ACCESS_LOG_DIR = "/var/log/"

def create_bandersnatch_conf():
    bs_default_conf = ''.join([CONF_FILE_PREFIX, "-default.conf"])
    bs_debug_conf = ''.join([CONF_FILE_PREFIX, "-debug.conf"])
    bs_log_conf = ''.join([CONF_FILE_PREFIX, "-log.conf"])
    bs_conf = ''.join([CONF_FILE_PREFIX, ".conf"])
    bs_bin = os.path.join(BANDERSNATCH_ENV_DIR, "bin/bandersnatch")

    if not os.path.isfile(bs_default_conf):
        call([bs_bin, "-c", bs_default_conf, "mirror"])

    parser = SafeConfigParser()
    parser.read(bs_default_conf)
    parser.set("mirror", "directory", os.path.join(MIRROR_DIR, "pypi"))
    parser.set("mirror", "workers", "6")
    parser.set("statistics", "access-log-pattern",
               os.path.join(ACCESS_LOG_DIR, "pypi.mirrors.access.*.log"))

    with open(bs_debug_conf, 'w') as fp:
        parser.write(fp)

    parser.set("mirror", "log-config", bs_log_conf)
    with open(bs_conf, 'w') as fp:
        parser.write(fp)


def create_bandersnatch_log_conf():
    bs_log_conf = ''.join([CONF_FILE_PREFIX, "-log.conf"])
    pypi_error_log = os.path.join(LOG_DIR, "pypi_error.log")

    parser = SafeConfigParser()
    parser.add_section("loggers")
    parser.set("loggers", "keys", "root, bandersnatch")

    parser.add_section("handlers")
    parser.set("handlers", "keys", "fileHandler")

    parser.add_section("formatters")
    parser.set("formatters", "keys", "simpleFormatter")

    parser.add_section("formatter_simpleFormatter")
    parser.set("formatter_simpleFormatter", "class", "logging.Formatter")
    parser.set("formatter_simpleFormatter", "format", "%(asctime)s %(levelname)s: %(message)s")
    # parser.set("formatter_simpleFormatter", "datefmt", "")

    parser.add_section("logger_root")
    parser.set("logger_root", "level", "ERROR")
    parser.set("logger_root", "handlers", "fileHandler")

    parser.add_section("logger_bandersnatch")
    parser.set("logger_bandersnatch", "level", "ERROR")
    parser.set("logger_bandersnatch", "handlers", "fileHandler")
    parser.set("logger_bandersnatch", "qualname", "bandersnatch")

    parser.add_section("handler_fileHandler")
    parser.set("handler_fileHandler", "class", "FileHandler")
    parser.set("handler_fileHandler", "formatter", "simpleFormatter")
    file_handler_args = ''.join(["(\"", pypi_error_log, "\", 'a')"])
    parser.set("handler_fileHandler", "args", file_handler_args)

    with open(bs_log_conf, 'w') as fp:
        parser.write(fp)


def install_virtualenv():
    call(["sudo", "pip", "install", "--upgrade", "virtualenv"])


def create_bandersnatch_env():
    pip_bin = os.path.join(BANDERSNATCH_ENV_DIR, "bin/pip")

    call(["virtualenv", BANDERSNATCH_ENV_DIR])
    call([pip_bin, "install", "-r",
          "https://bitbucket.org/pypa/bandersnatch/raw/stable/requirements.txt"])


def main():
    install_virtualenv()
    create_bandersnatch_env()
    create_bandersnatch_conf()
    create_bandersnatch_log_conf()


def test():
    create_bandersnatch_log_conf()


if __name__ == "__main__":
    main()
