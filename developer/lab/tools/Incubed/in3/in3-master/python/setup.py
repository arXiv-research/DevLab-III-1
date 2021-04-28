import pathlib
import setuptools
from os import environ

"""
Information on how to build this file
https://pypi.org/
https://pypi.org/classifiers/
"""


version = environ.get("version", "2.3.0")
url = environ.get("url", "https://github.com/blockchainsllc/in3")
License = environ.get("license", "AGPL")
description = environ.get(
    "description", "Incubed client and provider for web3. Based on in3-c runtime.")
keywords = environ.get(
    "keywords", "in3,c,arm,x86,x64,macos,windows,linux,blockchain,ethereum,bitcoin,ipfs").split(",")
readme = (pathlib.Path(__file__).parent / "README.md").read_text()
name = environ.get("name", "in3")
author = environ.get("author", "github.com/blockchainsllc/in3")
author_email = environ.get("author_email", "products@slock.it")
setuptools.setup(
    name=name,
    version=version,
    author=author,
    author_email=author_email,
    description=description,
    long_description=readme,
    long_description_content_type="text/markdown",
    url=url,
    packages=setuptools.find_packages(exclude=["docs", "tests"]),
    install_requires=[],
    keywords=keywords,
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Intended Audience :: Science/Research",
        "Environment :: Console",
        "Development Status :: 4 - Beta"
    ]
)
