import os

from setuptools import setup, find_packages

this_dir = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(this_dir, "README.md"), "r") as f:
    long_description = f.read()

setup(
    name="layab",
    version=open("layab/version.py").readlines()[-1].split()[-1].strip("\"'"),
    author="Colin Bounouar",
    author_email="colin.bounouar.dev@gmail.com",
    maintainer="Colin Bounouar",
    maintainer_email="colin.bounouar.dev@gmail.com",
    url="https://colin-b.github.io/layab/",
    description="Provide helper for REST API related stuff.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    download_url="https://pypi.org/project/layab/",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Build Tools",
    ],
    keywords=["flask"],
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        # Used to manage endpoints and swagger
        "flask-restplus==0.13.*",
        # Used to parse configurations
        "PyYAML==5.*",
        # Cross Origin handling
        "flask_cors==3.*",
        # Used to gz compress http output
        "flask_compress==1.*",
    ],
    extras_require={
        "testing": [
            # Used to manage testing of a Flask application
            "pytest-flask==0.15.*",
            # Used to check coverage
            "pytest-cov==2.*",
        ],
    },
    python_requires=">=3.6",
    project_urls={
        "GitHub": "https://github.com/Colin-b/layab",
        "Changelog": "https://github.com/Colin-b/layab/blob/master/CHANGELOG.md",
        "Issues": "https://github.com/Colin-b/layab/issues",
    },
    platforms=["Windows", "Linux"],
)
