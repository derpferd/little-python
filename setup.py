from setuptools import setup

# TODO: add better metadata https://python-packaging.readthedocs.io/en/latest/metadata.html

setup(name='littlepython',
      version='0.2.0',
      description='A Super Simplified Python with a Little Syntactic Sugar',
      url='https://github.com/DerPferd/little-python',
      author='Jonathan Beaulieu',
      author_email='123.jonathan@gmail.com',
      license='MIT',
      packages=['littlepython'],
      zip_safe=False,
      test_suite='nose.collector',
      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      scripts=['bin/littlepy'])
