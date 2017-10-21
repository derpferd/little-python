from setuptools import setup
from distutils.util import convert_path

# TODO: add better metadata https://python-packaging.readthedocs.io/en/latest/metadata.html

# Hack to get around version dependency problems
# Taken from: https://stackoverflow.com/a/24517154
main_ns = {}
ver_path = convert_path('littlepython/version.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)


setup(name='littlepython',
      version=main_ns["version"],
      description='A Super Simplified Python with a Little Syntactic Sugar',
      url='https://github.com/DerPferd/little-python',
      author='Jonathan Beaulieu',
      author_email='123.jonathan@gmail.com',
      license='MIT',
      packages=['littlepython'],
      zip_safe=False,
      test_suite='nose.collector',
      install_requires=['enum34;python_version<"3.4"'],
      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      scripts=['bin/littlepy'])
