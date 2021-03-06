# -*- coding: utf-8 -*-
""" Installer for the forests.content package.
"""
from os.path import join
from setuptools import find_packages
from setuptools import setup


long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CONTRIBUTORS.rst').read(),
    open(join("docs", "HISTORY.txt")).read(),
])

NAME = 'forests.theme'
PATH = ['src'] + NAME.split('.') + ['version.txt']
VERSION = open(join(*PATH)).read().strip()

setup(
    name=NAME,
    version=VERSION,
    description="FORESTS Theme",
    long_description_content_type="text/x-rst",
    long_description=long_description,
    # Get more from https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords='Python Plone',
    author='"EEA: IDM2 S-Team"',
    author_email='Christian.Prosperini@eea.europa.eu',
    url='https://pypi.python.org/pypi/forests.theme',
    license='GPL version 2',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['forests'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'plone.api',
        'plone.app.contenttypes',
        'pas.plugins.ldap',
        'z3c.jbot',
        'z3c.formwidget.optgroup >= 1.3rc1',
    ],
    extras_require={
        'test': [
            'plone.app.testing',
        ],
    },
)
