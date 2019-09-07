import os
import sys
import tempfile
import shutil
import pathlib

from photo_backup.handling import backup_file

sys.path.insert(0,
                os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


DIR_PATH = os.path.dirname(os.path.realpath(__file__))


def test_handling():
    with tempfile.TemporaryDirectory() as srcdir:
        # Create simple source directory structure.
        subdir_name = "subdir"
        file_name = "testfile.jpg"
        subdir = os.path.join(srcdir, subdir_name)
        os.mkdir(subdir)
        shutil.copy(os.path.join(DIR_PATH, file_name), subdir)
        print(subdir)

        # Backup the file so that first level sub-directory is retained.
        with tempfile.TemporaryDirectory() as destdir:
            print(destdir)
            print(len(pathlib.Path(srcdir).parts))
            backup_file(subdir, file_name, destdir,
                        len(pathlib.Path(srcdir).parts))
            print(os.listdir(destdir))
            assert os.path.isfile(os.path.join(destdir, subdir_name,
                                               file_name))
