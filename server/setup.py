from setuptools import setup, find_packages

setup(
    name="peakdb",
    version="0.0.1",
    description=("A simple module."),
    packages=find_packages(exclude=["tests"]),
)