"""
Call "pip install ." to initialize
Call "pip install -e ." for local development, see also requirements.txt
"""

import setuptools

setuptools.setup(
    name="wordle-bechmark",
    version="1.0",
    description="Python Distribution Utilities",
    author="Peter Bryan",
    author_email="peterbbryan@gmail.com",
    packages=setuptools.find_packages(),
)
