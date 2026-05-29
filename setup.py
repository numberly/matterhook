"""
matterhook
"""

import os

from setuptools import find_packages, setup


def read(fname: str):
    """Read README file
    Utility function to read the README file.
    Used for the long_description.  It's nice, because now 1) we have a top
    level README file and 2) it's easier to type in the README file than to
    put a raw string in below ...

    :param fname: README filename
    :type fname: str
    :return: File contents
    :rtype: str
    """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    author="numberly",
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    description="Interact with Mattermost incoming webhooks easily.",
    download_url="https://github.com/numberly/matterhook/tags",
    include_package_data=True,
    install_requires=[],
    license="BSD",
    long_description=read("README.rst"),
    name="matterhook",
    packages=find_packages(),
    platforms="any",
    url="https://github.com/numberly/matterhook",
    version="0.3",
    zip_safe=True,
)
