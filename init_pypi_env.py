#!/usr/bin/env python

from subprocess import call

def create_bandersnatch_conf():
    call(["mv", "bandersnatch-template.conf", "bandersnatch/bandersnatch-debug.conf"])


def install_virtualenv():
    call(["sudo", "pip", "install", "--upgrade", "virtualenv"])


def create_bandersnatch_env():
    call(["virtualenv", "bandersnatch"])
    # call(["cd", "bandersnatch"])
    call(["bandersnatch/bin/pip", "install", "-r",
          "https://bitbucket.org/pypa/bandersnatch/raw/stable/requirements.txt"])


def main():
    install_virtualenv()
    create_bandersnatch_env()
    create_bandersnatch_conf()


if __name__ == "__main__":
    main()
