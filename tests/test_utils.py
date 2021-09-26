import os
import sys

from photo_backup.utils import check_suffix

sys.path.insert(0,
                os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def test_suffix_none():
    assert check_suffix(None, None)


def test_suffix_positive():
    assert check_suffix("foo.bar", ["bar"])
    assert check_suffix("foo.bar", ["x", "bar", "y"])


def test_suffix_negative():
    assert not check_suffix("foo.bar", ["x", "y", "foo", "z"])
