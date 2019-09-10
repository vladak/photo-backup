
[![Github Actions status](https://github.com/vladak/photo-backup/workflows/Main%20workflow/badge.svg)](https://github.com/vladak/photo-backup) [![Build Status](https://travis-ci.com/vladak/photo-backup.svg?branch=master)](https://travis-ci.com/vladak/photo-backup) [![codecov](https://codecov.io/gh/vladak/photo-backup/branch/master/graph/badge.svg)](https://codecov.io/gh/vladak/photo-backup)

Set of scripts that facilitate easy(ier) backup of directory tree with photos.
Even though I have quite solid backup strategy for local backups, I wanted to
have the most valuable photos backed up remotely. This set of script creates
subtree of directory tree with photos which can then be synced elsewhere.

# Install

Create Python virtual environment and install the dependencies:

```
python3 -m venv create venv
. ./venv/bin/activate
pip  install --upgrade pip
python setup.py install
```

Use e.g. like this:

```
./venv/bin/photobackup -s JPG -s jpg -k nice -k selected srcDir dstDir
```

or from crontab:

```
# run five minutes after midnight, every Sunday
5 0 * * $HOME/photo-backup/venv/bin/python $HOME/photo-backup/venv/bin/photobackup -l WARNING ...
```
