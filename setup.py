#!/usr/bin/env python3
"""
Setup script for Circle Code System
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="circle-code",
    version="1.0.0",
    author="Circle Code Team",
    author_email="team@circlecode.dev",
    description="A revolutionary circular alternative to QR codes",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/circlecode/circlecode",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Scientific/Engineering :: Image Processing",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
        "docs": [
            "sphinx>=4.0",
            "sphinx-rtd-theme>=1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "circlecode=cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="qr-code, barcode, circular, encoding, computer-vision, opencv",
    project_urls={
        "Bug Reports": "https://github.com/circlecode/circlecode/issues",
        "Source": "https://github.com/circlecode/circlecode",
        "Documentation": "https://circlecode.readthedocs.io/",
    },
) 