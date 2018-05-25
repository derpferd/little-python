from setuptools import setup
from distutils.util import convert_path


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
      setup_requires=[],
      tests_require=['pytest', 'pytest-runner', 'pytest-timeout'],
      scripts=['bin/littlepy'],
      classifiers=[
            # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
            "Development Status :: 3 - Alpha",
            "License :: OSI Approved :: MIT License",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
      ]
      )
