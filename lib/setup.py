from distutils.core import setup

from predictionio import __version__
from predictionio import __author__
from predictionio import __email__


setup(name='PredictionIO-Python-SDK', 
      version=__version__,
      author=__author__,
      author_email=__email__,
      packages=['predictionio'],
      url = 'http://prediction.io',
      license='LICENSE.txt',
      description='PredictionIO Python SDK',
      long_description='PredictionIO Python SDK',
      #install_requires=[],
      )
