from setuptools import setup, find_packages

VERSION = "2023.05.17.1"
DESCRIPTION = "The Python package for accountants."
LONG_DESCRIPTION = "Cpya is a useful Python package that allows you utilize many essential accounting functions with " \
                   "ease!"

setup(
    name="cpya_jacobzufall",
    version=VERSION,
    author="Jacob Zufall",
    author_email="jacobzufall@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],

    keywords=[
        "python:",
        "first package"
    ],

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
