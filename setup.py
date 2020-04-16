import setuptools
from pip.req import parse_requirements

"""
python3 setup.py bdist_wheel
pip3 install -I dist/
"""

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ffmpeg-streams-manager",
    version='0.0.1',
    author="Anthony K GROSS",
    author_email="anthony.k.gross@gmail.com",
    description="Manage your streams via ffmpeg",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/anthonykgross/ffmpeg-streams-manager",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[str(ir.req) for ir in parse_requirements('requirements.txt', session='hack')]
)