from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["numpy>=1.22.3"]

setup(
    name="probability-models",
    version="0.0.1",
    author="Joseph Giordano",
    author_email="joeydanodano@gmail.com",
    description="A package to run numerical simulations for markov processes and random walks",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/joeygiordano13/probability-models/",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)