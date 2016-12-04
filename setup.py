
from setuptools import find_packages, setup

setup(name='student_retainer',
      version='0.1',
      description='Python/R-based program with GUI to predict student success',
      author='Timothy Burt, Melie Lewis, Koby Pascual, Yutian Tang',
      author_email='timcantango@gmail.com',
      url='https://github.com/tab10/student_retainer',
      packages=find_packages(),
      install_requires=['numpy', 'matplotlib', 'numericalunits', 'rpy2'], )