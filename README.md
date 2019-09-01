
Set of scripts that facilitate easy(ier) backup of directory tree with photos.
Even though I have quite solid backup strategy for local backups, I wanted to
have the most valuable photos backed up remotely. This set of script creates
subtree of directory tree with photos which can then be synced elsewhere.

# Install

Create Python virtual environment and install the dependencies:

```
python3 -m venv create venv
pip  install --upgrade pip
pip install -r requirements.txt
. ./venv/bin/activate
```

Use e.g. like this:

```
./exifkeyword_diftree.py -s JPG -s jpg -k nice -k selected srcDir dstDir
```
