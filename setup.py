from setuptools import setup

# TODO: add better metadata https://python-packaging.readthedocs.io/en/latest/metadata.html

setup(name='littlepy',
    version='0.1',
    description='A Super Simplified Python with a Little Syntactic Sugar',
    url='https://github.com/DerPferd/little-python',
    author='Jonathan Beaulieu',
    author_email='123.jonathan@gmail.com',
    license='MIT',
    packages=['littlepy'],
    zip_safe=False,
    test_suite='nose.collector',
    tests_require=['nose'],
    scripts=['bin/littlepy'])