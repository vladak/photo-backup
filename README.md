
Set of scripts that facilitate easy(ier) backup of directory tree with photos.
Even though I have quite solid backup strategy for local backups, I wanted to
have the most valuable photos backed up remotely. This set of script creates
subtree of directory tree with photos and performs backup to a cloud based
provider (currently Dropbox).

# Requirements

The script requires:
  - exiftool Python module

# Usage

Use e.g. like this:

```
./exifkeyword_diftree.py -s JPG -s jpg -k nice -k selected srcDir dstDir
```
