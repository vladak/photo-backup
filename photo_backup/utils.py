import os
import sys
import logging


def check_dir(name):

    logger = logging.getLogger(__name__)

    logger.debug("Checking '{}' if is a directory".format(name))

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
    if suffixes is None:
        return True

    for suffix in suffixes:
        if filename.endswith('.{}'.format(suffix)):
            return True

    return False
