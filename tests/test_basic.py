import exiftool
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from photo_backup.exif import check_keywords

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

class BasicTests(unittest.TestCase):

    def test_check_keywords(self):
        with exiftool.ExifTool() as et:
            assert check_keywords(et, os.path.join(DIR_PATH, "testfile.jpg"), ["selected"])
            assert not check_keywords(et, os.path.join(DIR_PATH, "testfile.jpg"), ["foo"])
