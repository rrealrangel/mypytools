from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
     name='mypytools',
     version='0.2.6.3.1',
     author='R. A. Real-Rangel',
     author_email='rrealr@iingen.unam.mx',
     description='Conjunto de rutinas que uso a cada rato.',
     license='GPL-3.0',
     keywords="herramientas general personal",
     url='https://bitbucket.org/pysdi/pysdi',
     packages=['mypytools'],
     long_description=long_description,
     long_description_content_type='text/markdown',
     classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Scientific/Engineering :: Hydrology",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
        ],
     install_requires=[
         'datetime',
         'dask',
         'netcdf4',
         'numpy',
         'pathlib2',
         'scipy',
         'toml',
         'toolz',
         'xarray',
         ],
     zip_safe=False
     )
