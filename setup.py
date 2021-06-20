from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='mcc-mnc',
    version='1.0.0',
    packages=['src'],
    url='https://github.com/jbjulia/mcc-mnc',
    license='MIT',
    author='Joseph Julian',
    author_email='joseph.b.julian@gmail.com',
    description='Mobile Country Codes (MCC) and Mobile Network Codes (MNC)',
    long_description=long_description
)
