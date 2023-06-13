from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="mccmnc",
    version="3.3",
    author="Joseph Julian",
    author_email="jbjulian@pm.me",
    description="A tool for matching and retrieving information about MCC-MNC combinations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jbjulia/mcc-mnc",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=["beautifulsoup4", "tqdm"],
    entry_points={
        "console_scripts": [
            "mccmnc=mccmnc.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
