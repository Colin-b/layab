<h2 align="center">Layab: Wonderful REST API</h2>

<p align="center">
<a href="https://pypi.org/project/layab/"><img alt="pypi version" src="https://img.shields.io/pypi/v/layab"></a>
<a href="https://travis-ci.org/Colin-b/layab"><img alt="Build status" src="https://api.travis-ci.org/Colin-b/layab.svg?branch=develop"></a>
<a href="https://travis-ci.org/Colin-b/layab"><img alt="Coverage" src="https://img.shields.io/badge/coverage-100%25-brightgreen"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://travis-ci.org/Colin-b/layab"><img alt="Number of tests" src="https://img.shields.io/badge/tests-51 passed-blue"></a>
<a href="https://pypi.org/project/layab/"><img alt="Number of downloads" src="https://img.shields.io/pypi/dm/layab"></a>
</p>

Layab stands for Wonderful in Somali and is also a shortcut for Layabout (we all are).

This package provides the following features:

## YAML Configuration ##

API configuration and logging configuration can be standardized.

### Loading configuration ###

```python
import layab

# Load logging and service configuration
service_configuration = layab.load('path/to/a/file/in/module/folder')
```

Note that in case your logging configuration file contains execution of Python code, you will need to provide the `yaml.UnsafeLoader` loader.

```python
import layab
import yaml

# Load logging and service configuration
service_configuration = layab.load('path/to/a/file/in/module/folder', logging_loader=yaml.UnsafeLoader)
```

## Flask RestPlus ##

The way your REST API behaves can be standardized

### Default behavior ###

Importing layab will make sure that every flask request is logged on reception. 

```python
import layab
```

## How to install
1. [python 3.6+](https://www.python.org/downloads/) must be installed
2. Use pip to install module:
```sh
python -m pip install layab
```
