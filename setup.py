from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='codequery',
    version='0.1.4',
    description='Queries and code facts checking support for python source code',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/daltonserey/codequery',
    author='Dalton Serey',
    author_email='daltonserey@gmail.com',
    maintainer='Dalton Serey',
    maintainer_email='daltonserey@gmail.com',
    license='MIT',
    packages=find_packages(),
    python_requires='>3.6',
    scripts=[
        'codequery/code-outline',
        'codequery/code-profile',
    ],
)
