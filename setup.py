from setuptools import setup, find_packages # Always prefer setuptools over distutils
from codecs import open # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='rusmarc',
    version='0.1a0',
    description='RUSMARC manipulation library',
    long_description=long_description,

    url='https://github.com/pypa/rusmarc',

    author='loge',
    author_email='loge@int32.ru',

    license='MIT',
    classifiers=[
    # How mature is this project? Common values are
    # 3 - Alpha
    # 4 - Beta
    # 5 - Production/Stable
    'Development Status :: 3 - Alpha',
    # Indicate who your project is intended for
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries',
    # Pick your license as you wish (should match "license" above)
    'License :: OSI Approved :: MIT License',
    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    ],
    # What does your project relate to?
    keywords='RUSMARC MARC ISO 2709 bibliography library development',
    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=['rusmarc'],
)
