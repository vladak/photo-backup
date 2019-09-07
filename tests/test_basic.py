import exiftool
import os
import sys

from photo_backup.exif import check_keywords, get_keywords

sys.path.insert(0,
                os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


DIR_PATH = os.path.dirname(os.path.realpath(__file__))


def test_check_keywords():
    with exiftool.ExifTool() as et:
        assert check_keywords(et, os.path.join(DIR_PATH, "testfile.jpg"),
                              ["selected"])
        assert not check_keywords(et, os.path.join(DIR_PATH, "testfile.jpg"),
                                  ["nonexistent"])


def test_get_keywords():
    with exiftool.ExifTool() as et:
        assert get_keywords(et, os.path.join(DIR_PATH, "testfile.jpg")) == \
            ["selected"]
        assert get_keywords(et, os.path.join(DIR_PATH, "2keywords.jpg")) == \
            ["selected", "foo"]
        assert get_keywords(et, os.path.join(DIR_PATH, "nokeywords.jpg")) == []
