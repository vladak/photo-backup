from setuptools import setup

setup(
   name='photo_backup',
   version='1.3',
   description='Backup a directory tree of photos, filtering on EXIF keywords',
   author='Vladimir Kotal',
   author_email='vlada@devnull.cz',
   packages=['photo_backup'],
   install_requires=['exifread', 'filelock'],
   entry_points={
      'console_scripts': [
         'photobackup = photo_backup.photobackup:main'
      ]
   },
   tests_require=[
      'pytest',
      'pytest-cov',
   ],
)
