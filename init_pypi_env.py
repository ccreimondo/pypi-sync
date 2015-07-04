#!/usr/bin/env python

import os.path

from ConfigParser import SafeConfigParser
from subprocess import call

dirname = os.path.dirname(__file__)
file_prefix = "bandersnatch/bandersnatch"


def create_bandersnatch_conf():
    if not os.path.isfile("bandersnatch/bandersnatch-default.conf"):
        call(["bandersnatch/bin/bandersnatch",
              "-c", "bandersnatch/bandersnatch-default.conf", "mirror"])

    parser = SafeConfigParser()
    parser.read("bandersnatch/bandersnatch-default.conf")
    parser.set("mirror", "directory", "/www/mirrors/pypi")
    parser.set("mirror", "workers", "10")
    parser.set("statistics", "access-log-pattern",
                     "/var/log/pypi.mirrors.access.*.log")

    with open(os.path.join(dirname, ''.join([file_prefix, "-debug.conf"])), 'w') as fp:
        parser.write(fp)

    parser.set("mirror", "log-config",
                     "/www/mirrors/bin/bandersnatch/bandersnatch-log.conf")
    with open(os.path.join(dirname, ''.join([file_prefix, ".conf"])), 'w') as fp:
        parser.write(fp)


def create_bandersnatch_log_conf():
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

    parser.add_section("handler_fileHandler")
    parser.set("handler_fileHandler", "class", "FileHandler")
    parser.set("handler_fileHandler", "formatter", "simpleFormatter")
    parser.set("handler_fileHandler", "args", "(\"/www/mirrors/log/pypi_error.log\", 'a')")

    with open(os.path.join(dirname, ''.join([file_prefix, "-log.conf"])), 'w') as fp:
        parser.write(fp)


def install_virtualenv():
    call(["sudo", "pip", "install", "--upgrade", "virtualenv"])


def create_bandersnatch_env():
    call(["virtualenv", "bandersnatch"])
    call(["bandersnatch/bin/pip", "install", "-r",
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
    # test()
