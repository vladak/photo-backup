import os
import sys
import tempfile
import shutil
import pathlib
import exiftool

from photo_backup.backup import backup_file, backup_dir

sys.path.insert(0,
                os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


DIR_PATH = os.path.dirname(os.path.realpath(__file__))


def test_backup_file():
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


def get_list_of_files(dir_name):
    """
    :param dir_name: directory path
    :return: list of relative file paths under the directory
    """
    listOfFiles = list()

    for (dirpath, dirnames, filenames) in os.walk(dir_name):
        ln = len(os.path.commonprefix([dirpath, dir_name])) + 1
        listOfFiles += [os.path.join(dirpath[ln:], file) for file in filenames]

    return listOfFiles


def test_backupdir():
    with tempfile.TemporaryDirectory() as srcdir:
        # Create simple source directory structure.
        for subdir_name, filename in [("foo", "testfile.jpg"),
                                      ("bar", "2keywords.jpg"),
                                      ("wow", "nokeywords.jpg")]:
            subdir = os.path.join(srcdir, subdir_name)
            os.mkdir(subdir)
            shutil.copy(os.path.join(DIR_PATH, filename), subdir)

        # Backup the files so that first level sub-directory is retained.
        with tempfile.TemporaryDirectory() as destdir:
            print(destdir)
            print(len(pathlib.Path(srcdir).parts))
            with exiftool.ExifTool() as et:
                backup_dir(srcdir, destdir, True, et, ["selected"],
                           len(pathlib.Path(srcdir).parts), ["jpg"])
                assert set(get_list_of_files(destdir)) == \
                    set(['foo/testfile.jpg', 'bar/2keywords.jpg'])
