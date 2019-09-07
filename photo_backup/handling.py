import pathlib
import shutil
import os
import logging

from .exif import check_keywords
from .utils import check_suffix


def handle_file(args, dir_name, docopy, et, filename, logger):
    if not check_suffix(filename, args.suffix):
        logger.debug("Skipping {} due to no suffix match".
                     format(filename))
        return

    fullname = os.path.join(dir_name, filename)
    if not check_keywords(et, fullname, args.keyword):
        logger.debug("Skipping {} because it does not match any keyword".
                     format(fullname))
        return

    # TODO: collect runtime parameters into a class and
    #  pass its instance to avoid long argument list
    backup_file(dir_name, filename,
                args.destDir,
                args.stripcount, docopy)


def backup_file(dirname, filename, destdir,
                stripcount, copy=True):
    """
    :param dirname: directory path
    :param filename: file name
    :param destdir: destination directory path
    :param stripcount: how many path components to strip from dirname
    :param copy: boolean indicating whether to copy the file or create symlink
    """

    logger = logging.getLogger(__name__)

    fullname = os.path.join(dirname, filename)
    logger.debug('\t%s' % fullname)

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

