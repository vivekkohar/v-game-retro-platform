#!/usr/bin/env python3
"""
Setup script for Retro Platform Fighter - Diamond Quest
"""

from setuptools import setup, find_packages
import os

# Read the README file for long description
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements from requirements.txt
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="retro-platform-fighter",
    version="2.0.0",
    author="Game Developer",
    author_email="developer@example.com",
    description="A classic 2D platformer game with 10 challenging levels and power-ups",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/username/retro-platform",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Games/Entertainment :: Arcade",
        "Topic :: Games/Entertainment :: Side-Scrolling/Arcade Games",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "retro-platform=retro_platform_game:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["sounds/*.wav", "*.md", "requirements.txt"],
    },
    keywords="game platformer 2d pygame retro arcade",
    project_urls={
        "Bug Reports": "https://github.com/username/retro-platform/issues",
        "Source": "https://github.com/username/retro-platform",
        "Documentation": "https://github.com/username/retro-platform/blob/main/README.md",
    },
)
