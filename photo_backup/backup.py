import pathlib
import shutil
import os
import logging

from .exif import check_keywords
from .utils import check_suffix


def handle_file(dir_name, filename, destdir, docopy,
                et, keywords, stripcount, suffix):
    """
    Check if file is eligible for backup and if yes, back it up.
    :param dir_name: source directory
    :param filename: source file name
    :param destdir: destination directory
    :param docopy: copy or create symlink
    :param et: exiftool instance
    :param keywords: list of EXIF keywords
    :param stripcount: count of how many path components to strip from
    source directory
    :param suffix: suffixes to check
    """

    logger = logging.getLogger(__name__)

    if not check_suffix(filename, suffix):
        logger.debug("Skipping {} due to no suffix match".
                     format(filename))
        return

    # If the destination file already exists, do not copy.
    path = pathlib.Path(dir_name)
    dstdirname = os.path.sep.join(path.parts[int(stripcount):])
    dstname = os.path.join(destdir, dstdirname, filename)
    if os.path.exists(dstname):
        logger.debug("File {} already exists, skipping".
                     format(dstname))
        return

    # This is quite expensive operation as it involves reading EXIF data
    # from the file.
    fullname = os.path.join(dir_name, filename)
    if not check_keywords(et, fullname, keywords):
        logger.debug("Skipping {} because it does not match any keyword".
                     format(fullname))
        return

    backup_file(dir_name, filename, dstname, docopy)


def backup_file(dirname, filename, dstname, copy=True):
    """
    :param dirname: source directory path
    :param filename: source file name
    :param dstname: destination file
    :param copy: boolean indicating whether to copy the file or create symlink
    """

    logger = logging.getLogger(__name__)

    fullname = os.path.join(dirname, filename)
    logger.debug('\t%s' % fullname)

    dstdir = os.path.dirname(dstname)
    if not os.path.isdir(dstdir):
        logger.info('Creating directory: {}'.format(dstdir))
        os.makedirs(dstdir, exist_ok=True)

    if copy:
        logger.info("Copying {} to {}".format(fullname, dstname))
        shutil.copy(fullname, dstname)
    else:
        logger.info("Creating symlink {} -> {}".
                    format(dstname, fullname))
        os.symlink(fullname, dstname)


def backup_dir(source_dir, dest_dir, docopy, et, keywords,
               stripcount, suffixes):

    logger = logging.getLogger(__name__)

    for dirName, _, fileList in os.walk(source_dir):
        if not docopy and dirName == dest_dir:
            logger.debug("Skipping {}".format(dirName))
            continue

        logger.debug('Found directory: %s' % dirName)
        for filename in fileList:
            handle_file(dirName, filename, dest_dir, docopy,
                        et, keywords, stripcount,
                        suffixes)
