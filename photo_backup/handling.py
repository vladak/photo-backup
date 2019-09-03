import pathlib
import shutil
import os

from .exif import check_keywords
from .utils import check_suffix


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
