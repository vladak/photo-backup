import os
import sys
import tempfile
import shutil
import pathlib

from photo_backup.backup import backup_file, backup_dir, handle_file

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


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
            backup_file(subdir, file_name,
                        os.path.join(destdir, subdir_name, file_name))
            print(os.listdir(destdir))
            assert os.path.isfile(os.path.join(destdir, subdir_name,
                                               file_name))


def test_handle_file_no_suffix_match():
    # white-box testing: if handle_file() went further than the keyword check,
    # it would end with exception due to some parameters being None.
    with tempfile.TemporaryDirectory() as destdir:
        assert not handle_file(DIR_PATH, "testfile.jpg", destdir, True,
                               None, 0, ["txt"])


def test_handle_file_metadata_match():
    # white-box testing: if handle_file() went further than the metadata check,
    # it would end with exception due to some parameters being None.
    filename = "testfile.jpg"
    suffix = filename[filename.rfind("."):]
    with tempfile.TemporaryDirectory() as destdir:
        # Backup the file first.
        dstfile = os.path.join(destdir, filename)
        backup_file(DIR_PATH, filename, dstfile)
        assert os.path.exists(dstfile)

        assert not handle_file(DIR_PATH, filename, destdir, True,
                               None, 0, suffix)


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
            backup_dir(srcdir, destdir, True, ["selected"],
                       len(pathlib.Path(srcdir).parts), ["jpg"])
            assert set(get_list_of_files(destdir)) == \
                set(['foo/testfile.jpg', 'bar/2keywords.jpg'])
