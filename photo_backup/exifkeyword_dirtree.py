#!/usr/bin/env python3

"""
Copy files from a directory tree that have given keyword in their EXIF data
to a new directory tree, optionally using symlinks.

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

from .utils import check_dir, check_suffix


def check_keywords(logger, et, fullname, keywords):
    """
    Check if file has contains specified EXIF keywords.
    :param fullname: full path to the file
    :param keywords: list of keywords
    :return: true if the file contains a keyword from the list
    """
    try:
        metadata = et.get_metadata(fullname)
        logger.debug("File {} metadata: {}".
                     format(fullname, metadata))
    except json.decoder.JSONDecodeError:
        logger.error("Cannot get metadata for {}".format(fullname))
        return

    try:
        file_keywords = metadata["IPTC:Keywords"]
        logger.debug("File {} has keywords: {}".
                     format(fullname, file_keywords))
    except KeyError:
        logger.debug("File {} does not contain keyword metadata".
                     format(fullname))
        return False

    for keyword in keywords:
        if keyword in file_keywords:
            logger.debug("File {} contains the '{}' keyword".
                         format(fullname, keyword))
            return True

    return False


def handle_file(logger, et, dirname, filename, destdir, suffixes,
                stripcount, keywords, copy=True):

    if not check_suffix(filename, suffixes):
        logger.debug("Skipping {} due to no suffix match".
                     format(filename))
        return

    fullname = os.path.join(dirname, filename)
    logger.debug('\t%s' % fullname)

    if check_keywords(logger, et, fullname, keywords):
        # If the destination file already exists, do not copy.
        path = pathlib.Path(dirname)
        dstdirname = os.path.sep.join(path.parts[int(stripcount):])
        dstname = os.path.join(destdir, dstdirname, filename)
        # TODO: compare at least file size
        if os.path.exists(dstname):
            logger.debug("File {} already exists, skipping".
                         format(dstname))
            return

        dstdir = os.path.dirname(dstname)
        if not os.path.isdir(dstdir):
            logger.info('Creating directory: {}'.format(dstdir))
            os.makedirs(dstdir, exist_ok=True)

        if copy:
            logger.debug("Copying {} to {}".format(fullname, dstname))
            shutil.copy(fullname, dstname)
        else:
            logger.debug("Creating symlink {} -> {}".
                         format(dstname, fullname))
            os.symlink(fullname, dstname)
    else:
        logger.debug("Skipping {} because it does not match any keyword".
                     format(fullname))


def main():
    parser = argparse.ArgumentParser(description='recreate directory '
                                                 'structure just '
                                                 'from files that match'
                                                 'certain criteria')

    parser.add_argument('sourceDir')
    parser.add_argument('destDir')
    parser.add_argument('-k', '--keyword', required=True, action='append',
                        help='EXIF keyword(s)')
    parser.add_argument('-D', '--debug', action='store_true',
                        help='Enable debug prints')
    parser.add_argument('-s', '--suffix', action='append',
                        help='Suffix(es) of the files to work on')
    parser.add_argument('-S', '--stripcount', default=1,
                        help='Number of path components to strip from '
                             'sourceDir')
    parser.add_argument('--symlink', action='store_true',
                        help='create symlinks instead of copying files')
    # TODO add log level arg

    args = parser.parse_args()

    # TODO avoid basicConfig
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    logger = logging.getLogger(os.path.basename(sys.argv[0]))

    if not args.keyword or len(args.keyword) == 0:
        logger.error("No keywords specified")
        sys.exit(1)

    check_dir(logger, args.sourceDir)
    check_dir(logger, args.destDir)

    docopy = True
    if args.symlink:
        docopy = False

    lock = filelock.FileLock(os.path.join(tempfile.gettempdir(),
                                          "{}.lock".format(sys.argv[0])))
    try:
        with lock.acquire(timeout=0):
            with exiftool.ExifTool() as et:
                for dirName, subdirList, fileList in os.walk(args.sourceDir):
                    if not docopy and dirName == args.destDir:
                        logger.debug("Skipping {}".format(dirName))
                        continue

                    logger.debug('Found directory: %s' % dirName)
                    for filename in fileList:
                        # TODO: collect runtime parameters into a class and
                        #  pass its instance to avoid long argument list
                        handle_file(logger, et, dirName, filename,
                                    args.destDir, args.suffix,
                                    args.stripcount, args.keyword, docopy)
    except filelock.Timeout:
        logger.warning("Already running, exiting.")
        sys.exit(1)

    logging.shutdown()


if __name__ == '__main__':
    main()
