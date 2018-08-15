#!/usr/bin/env python3

"""
Copy files from a directory tree that have given keyword in their EXIF data
to a new directory tree.

This can serve as a way how to extract valuable files out of photo collection.

vlada@devnull.cz, 2018
"""

import argparse
import json
import logging
import os
import pathlib
import shutil
import sys
import tempfile

import filelock

import exiftool


def check_dir(name):
    """Check if name is directory. If not, exit the program."""
    if not os.path.isdir(name):
        logger.critical("{} is not a directory".format(name))
        sys.exit(1)


def check_suffix(fname, suffixes):
    """
    Check if filename has a suffix out of a list
    :param fname: file name to check
    :param suffixes: list of suffixes (can be None)
    :return: true if filename's suffix matches on in the list
    """
    if not suffixes:
        return True

    for suffix in suffixes:
        if fname.endswith('.{}'.format(suffix)):
            return True

    return False


def check_keywords(fullname, keywords):
    """
    Check if file has contains specified EXIF keywords.
    :param fullname: full path to the file
    :param keywords: list of keywords
    :return: true if the file contains a keyword from the list
    """
    try:
        metadata = et.get_metadata(fullname)
        logger.debug("File {} metadata: {}".format(fullname, metadata))
    except json.decoder.JSONDecodeError:
        logger.error("Cannot get metadata for {}".format(fullname))
        return

    try:
        file_keywords = metadata["IPTC:Keywords"]
        logger.debug("File {} has keywords: {}".format(fullname, file_keywords))
    except KeyError:
        logger.debug("File {} does not contain keyword metadata".format(fullname))
        return False

    for keyword in keywords:
        if keyword in file_keywords:
            logger.debug("File {} contains the '{}' keyword".format(fullname, keyword))
            return True

    return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='recreate directory structure just from files that match'
                                                 'certain criteria')

    parser.add_argument('sourceDir')
    parser.add_argument('destDir')
    parser.add_argument('-k', '--keyword', required=True, action='append', help='EXIF keyword(s)')
    parser.add_argument('-D', '--debug', action='store_true',
                        help='Enable debug prints')
    parser.add_argument('-s', '--suffix', action='append', help='Suffix(es) of the files to work on')
    parser.add_argument('-S', '--stripcount', default=1, help='Number of path components to strip from sourceDir')

    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    logger = logging.getLogger(os.path.basename(sys.argv[0]))

    if not args.keyword or len(args.keyword) == 0:
        logger.error("No keywords specified")
        sys.exit(1)

    check_dir(args.sourceDir)
    check_dir(args.destDir)

    lock = filelock.FileLock(os.path.join(tempfile.gettempdir(),
                                          "{}.lock".format(sys.argv[0])))
    try:
        with lock.acquire(timeout=0):
            with exiftool.ExifTool() as et:
                for dirName, subdirList, fileList in os.walk(args.sourceDir):
                    logger.debug('Found directory: %s' % dirName)
                    for filename in fileList:
                        if not check_suffix(filename, args.suffix):
                            logger.debug("Skipping {}".format(filename))
                            continue

                        fullname = os.path.join(dirName, filename)
                        logger.debug('\t%s' % fullname)

                        if check_keywords(fullname, args.keyword):
                            path = pathlib.Path(dirName)
                            dstdirname = os.path.sep.join(path.parts[int(args.stripcount):])
                            dstname = os.path.join(args.destDir, dstdirname, filename)
                            dstdir = os.path.dirname(dstname)
                            logger.info('Creating directory: {}'.format(dstdir))
                            os.makedirs(dstdir, exist_ok=True)
                            logger.debug("Copying {} to {}".format(fullname, dstname))
                            shutil.copy(fullname, dstname)
                        else:
                            logger.debug("Skipping {} because it does not match any keyword".format(fullname))

    except filelock.Timeout:
        logger.warning("Already running, exiting.")
        sys.exit(1)

    logging.shutdown()