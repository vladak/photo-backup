#!/usr/bin/env python3

"""
Copy files from a directory tree that have given keyword in their EXIF data
to a new directory tree, optionally using symlinks.

This can serve as a way how to extract valuable files out of photo collection.

vlada@devnull.cz, 2018
"""

import argparse
import logging
import os
import sys
import tempfile

import filelock

import exiftool

from .utils import check_dir
from .handling import handle_file


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
                        handle_file(et, dirName, filename,
                                    args.destDir, args.suffix,
                                    args.stripcount, args.keyword, docopy)
    except filelock.Timeout:
        logger.warning("Already running, exiting.")
        sys.exit(1)

    logging.shutdown()


if __name__ == '__main__':
    main()