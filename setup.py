from setuptools import setup, find_packages # Always prefer setuptools over distutils
from codecs import open # To use a consistent encoding
from os import path

setup(
    name='arcplus',
    version='0.1',
    description="a few things missing from Esri's arcpy",
    url='https://github.com/maphew/arcplus',
    author='Matt Wilkie',
    author_email='maphew@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        ],
    keywords='arcpy, arcgis',
    install_requires=['comtypes'],
    )