from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()


def read(*rnames):
    return open(path.join(path.dirname(__file__), *rnames)).read()


setup(
     name='mypytools',
     version='1a.9',
     author='R. A. Real-Rangel',
     author_email='rrealr@iingen.unam.mx',
     description='Conjunto de rutinas que uso a cada rato.',
     license='GPL-3.0',
     keywords="herramientas general personal",
     url='https://github.com/rrealrangel/mypytools',
     packages=['mypytools'],
     long_description=long_description,
     long_description_content_type='text/markdown',
     classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
        ],
     install_requires=[
         'numpy',
         'pandas',
         'pathlib',
         'scipy',
         'sklearn',
         'statsmodels',
         'xarray'
         ],
     zip_safe=False
     )
