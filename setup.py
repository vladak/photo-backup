from setuptools import setup

setup(
   name='photo-backup',
   version='1.0',
   description='Create a directory tree of images based on EXIF keywords',
   author='Vladimir Kotal',
   author_email='vlada@devnull.cz',
   packages=['photo-backup'],
   install_requires=['PyExifTool', 'filelock'], #external packages as dependencies
   # scripts=['exifkeyword_dirtree.py']
)
