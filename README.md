<h2 align="center">Layab: Wonderful REST API</h2>

<p align="center">
<a href="https://pypi.org/project/layab/"><img alt="pypi version" src="https://img.shields.io/pypi/v/layab"></a>
<a href="https://travis-ci.org/Colin-b/layab"><img alt="Build status" src="https://api.travis-ci.org/Colin-b/layab.svg?branch=master"></a>
<a href="https://travis-ci.org/Colin-b/layab"><img alt="Coverage" src="https://img.shields.io/badge/coverage-100%25-brightgreen"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://travis-ci.org/Colin-b/layab"><img alt="Number of tests" src="https://img.shields.io/badge/tests-51 passed-blue"></a>
<a href="https://pypi.org/project/layab/"><img alt="Number of downloads" src="https://img.shields.io/pypi/dm/layab"></a>
</p>

Layab stands for `Wonderful` in Somali and is also a shortcut for `Layabout` (aren't we all lazy).

This package provides helper functions on top of [Flask-RestPlus](https://flask-restplus.readthedocs.io/en/stable/index.html) to create standardized REST API.

## Available features

- [API](#api)
- [Monitoring](#monitoring)
- [Configuration](#configuration)

### API

You can create a Flask application and a [Flask-RestPlus](https://flask-restplus.readthedocs.io/en/stable/index.html) API using the `layab.create_api` function.

```python
import layab

application, api = layab.create_api(
    __file__,
    title="My API",
    description="This is the purpose of my API",
)
```

### Monitoring

Importing layab will make sure that every flask request is logged as INFO upon reception and return (even in case an exception occurred). 

```python
import layab
```

You can add monitoring endpoints to your API using `layab.add_monitoring_namespace` function.

The following endpoints will then be available:
* `/health`: Providing Health of your API
* `/changelog`: Providing the changelog of your application so that clients can check what's new.

```python
import layab

api = None  # Replace with your Flask-RestPlus API instance

def health_details():
    # Health status, Health details
    return "pass", {}

layab.add_monitoring_namespace(api, health_details)
```

Should you need to check the status of an external HTTP service or a Redis connection, you can rely on [healthpy](https://pypi.org/project/healthpy/) to retrieve the health status and details.

Note that [healthpy](https://pypi.org/project/healthpy/) also handle the merging of multiple status into one.

### Configuration

API and logging configuration should be stored in YAML format.

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

## How to install
1. [python 3.6+](https://www.python.org/downloads/) must be installed
2. Use pip to install module:
```sh
python -m pip install layab
```
