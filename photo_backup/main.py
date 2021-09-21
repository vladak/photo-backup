#!/usr/bin/env python3

"""
Copy files from a directory tree that have given keyword in their EXIF data
to a new directory tree, optionally using symlinks.

This can serve as a way how to extract valuable files out of photo collection.

vlada@devnull.cz, 2018-2021
"""

import argparse
import logging
import os
import sys
import tempfile

import filelock

from .utils import check_dir
from .backup import backup_dir
from .log import LogLevelAction


def main():
    parser = argparse.ArgumentParser(description='recreate directory '
                                                 'structure just '
                                                 'from files that match'
                                                 'certain criteria')

    parser.add_argument('sourceDir')
    parser.add_argument('destDir')
    parser.add_argument('-k', '--keyword', required=True, action='append',
                        help='EXIF keyword(s)')
    parser.add_argument('-s', '--suffix', action='append',
                        help='Suffix(es) of the files to work on')
    parser.add_argument('-S', '--stripcount', default=1,
                        help='Number of path components to strip from '
                             'sourceDir')
    parser.add_argument('--symlink', action='store_true',
                        help='create symlinks instead of copying files')
    parser.add_argument('-l', '--loglevel', action=LogLevelAction,
                        help='Set log level (e.g. \"ERROR\")',
                        default=logging.INFO)

    try:
        args = parser.parse_args()
    except ValueError as e:
        print("Argument parsing failed: {}".format(e), file=sys.stderr)
        sys.exit(1)

    logger = logging.getLogger(__package__)
    logger.setLevel(args.loglevel)
    handler = logging.StreamHandler()
    logger.addHandler(handler)

    if not args.keyword or len(args.keyword) == 0:
        logger.error("No keywords specified")
        sys.exit(1)

    check_dir(args.sourceDir)
    check_dir(args.destDir)

    docopy = True
    if args.symlink:
        docopy = False

    lock = filelock.FileLock(os.path.join(tempfile.gettempdir(),
                                          "{}.lock".
                                          format(os.path.
                                                 basename(sys.argv[0]))))
    try:
        with lock.acquire(timeout=0):
            # To prevent iptcinfo3 from emitting warnings on files without
            # IPTC data.
            iptc_logger = logging.getLogger('iptcinfo')
            iptc_logger.setLevel(logging.ERROR)

            backup_dir(args.sourceDir, args.destDir, docopy,
                       args.keyword, args.stripcount, args.suffix)
    except filelock.Timeout:
        logger.warning("Already running, exiting.")
        sys.exit(1)

    logging.shutdown()
