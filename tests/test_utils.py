import os
import sys

import pytest

from photo_backup.utils import check_suffix, check_dir

sys.path.insert(0,
                os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def test_suffix_none():
    assert check_suffix(None, None)


def test_suffix_positive():
    assert check_suffix("foo.bar", ["bar"])
    assert check_suffix("foo.bar", ["x", "bar", "y"])


def test_suffix_negative():
    assert not check_suffix("foo.bar", ["x", "y", "foo", "z"])


def test_check_dir_negative():
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        check_dir("/nonexistent")
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
