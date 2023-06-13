from setuptools import setup, find_packages

VERSION = "2023.06.12.1"
DESCRIPTION = "The Python package for accountants."
LONG_DESCRIPTION = "TaxPy is a useful Python package that allows you utilize many essential accounting functions with " \
                   "ease!"

setup(
    name="taxpy",
    version=VERSION,
    author="Jacob Zufall",
    author_email="jacobzufall@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],

    keywords=[
        "python:",
    ],

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
