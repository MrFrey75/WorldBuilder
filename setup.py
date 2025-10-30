"""WorldBuilder package configuration."""
from setuptools import setup, find_packages

setup(
    name="worldbuilder",
    version="0.1.0",
    description="A comprehensive worldbuilding and universe creation tool",
    author="WorldBuilder Team",
    python_requires=">=3.11",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "PyQt6>=6.6.0",
        "SQLAlchemy>=2.0.0",
        "python-dateutil>=2.8.2",
        "Pillow>=10.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-qt>=4.2.0",
            "black>=23.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "worldbuilder=worldbuilder.main:main",
        ],
    },
)
