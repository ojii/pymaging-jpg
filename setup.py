# -*- coding: utf-8 -*-
from setuptools import setup
from pymaging_jpg import __version__

setup(
    name = "pymaging-jpg",
    version = __version__,
    packages = ['pymaging_jpg'],
    install_requires = ['pymaging'],
    entry_points = {'pymaging.formats': ['jpg = pymaging_jpg.jpg:JPG']},
    author = "Jonas Obrist",
    author_email = "ojiidotch@gmail.com",
    description = "JPG support for Pymaging",
    license = "BSD",
    keywords = "pymaging jpg imaging",
    url = "https://github.com/ojii/pymaging-jpg/",
    zip_safe = False,
    test_suite = 'pymaging_jpg.tests'
)
