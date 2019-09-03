import os
import sys


def check_dir(logger, name):
    """Check if name is directory. If not, exit the program."""
    if not os.path.isdir(name):
        logger.critical("{} is not a directory".format(name))
        sys.exit(1)


def check_suffix(filename, suffixes):
    """
    Check if filename has a suffix out of a list
    :param filename: file name to check
    :param suffixes: list of suffixes (can be None)
    :return: true if filename's suffix matches on in the list
    """
    if not suffixes:
        return True

    for suffix in suffixes:
        if filename.endswith('.{}'.format(suffix)):
            return True

    return False
