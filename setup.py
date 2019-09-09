from setuptools import setup

setup(
   name='photo_backup',
   version='1.2',
   description='Create a directory tree of images based on EXIF keywords',
   author='Vladimir Kotal',
   author_email='vlada@devnull.cz',
   packages=['photo_backup'],
   install_requires=['PyExifTool', 'filelock'],
   entry_points={
      'console_scripts': [
         'photobackup = photo_backup.photobackup:main'
      ]
   },
   tests_require=[
      'pytest',
   ],
)
