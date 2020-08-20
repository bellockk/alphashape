#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

requirements = ['Click>=6.0',
                'click_log>=0.3.2',
                'shapely>=1.4.0',
                'scipy>=1.0.0']

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Kenneth E. Bellock",
    author_email='ken@bellock.net',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Toolbox for generating alpha shapes.",
    entry_points={
        'console_scripts': [
            'alphashape=alphashape.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords='alphashape',
    name='alphashape',
    packages=find_packages(include=['alphashape']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/bellockk/alphashape',
    version='1.1.0',
    zip_safe=False,
)
