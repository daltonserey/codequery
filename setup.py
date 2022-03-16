from setuptools import setup
from pathlib import Path

cwd = Path(__file__).parent
long_description = (cwd / "README.md").read_text()

setup(
    name='codequery',
    version='0.1.0',
    description='Queries and code facts checking support for python source code',
    url='https://github.com/daltonserey/codequery',
    author='Dalton Serey',
    author_email='daltonserey@gmail.com',
    maintainer='Dalton Serey',
    maintainer_email='daltonserey@gmail.com',
    license='MIT',
    long_description=long_description,
    py_modules=['codequery'],
    python_requires='>3.6',
    install_requires=['pytest>=5.0.0'],
)
