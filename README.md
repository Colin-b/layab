<h2 align="center">Layab: Wonderful REST API</h2>

<p align="center">
<a href="https://pypi.org/project/layab/"><img alt="pypi version" src="https://img.shields.io/pypi/v/layab"></a>
<a href="https://travis-ci.com/Colin-b/layab"><img alt="Build status" src="https://api.travis-ci.com/Colin-b/layab.svg?branch=master"></a>
<a href="https://travis-ci.com/Colin-b/layab"><img alt="Coverage" src="https://img.shields.io/badge/coverage-100%25-brightgreen"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://travis-ci.com/Colin-b/layab"><img alt="Number of tests" src="https://img.shields.io/badge/tests-30 passed-blue"></a>
<a href="https://pypi.org/project/layab/"><img alt="Number of downloads" src="https://img.shields.io/pypi/dm/layab"></a>
</p>

Layab stands for `Wonderful` in Somali and is also a shortcut for `Layabout` (aren't we all lazy).

This package provides helper functions on top of [Starlette](https://www.starlette.io) to create standardized REST API.

If you were using layab 1.* (based on Flask-RestPlus), please refer to the [Migration guide](#migration-guide).

## Available features

- [Middleware](#middleware)
- [Configuration](#configuration)
- [Responses](#responses)

### Middleware

You can get a bunch of already created [Starlette middleware](https://www.starlette.io/middleware/) thanks to `layab.middleware` function.

```python
from starlette.applications import Starlette
import layab

app = Starlette(middleware=layab.middleware())
```

By default you will have the following [middleware](https://www.starlette.io/middleware/):
 * LoggingMiddleware: Log requests upon reception and return (failure or success).
 * CORSMiddleware: Allow cross origin requests.
 * ProxyHeadersMiddleware (requires [uvicorn](https://github.com/encode/uvicorn/blob/master/uvicorn/middleware/proxy_headers.py)): Handle requests passing by a reverse proxy.

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

### Responses

Default [responses](https://www.starlette.io/responses/) are available to return standard responses.

#### Location response
```python
from starlette.applications import Starlette
import layab

app = Starlette()

@app.route("/resource", methods=["POST", "PUT"])
def handle_resource(request):
    resource_id = create_update_resource()  # Implement this endpoint
    return layab.LocationResponse(request, "/resource/{resource_id}")

@app.route("/resource/{resource_id}", methods=["GET"])
def get_resource(request):
    pass  # Implement this endpoint
```

## Migration guide

### Created response

Layab 1.*

```python
import layab

api = None

@api.doc(**layab.created_response_doc(api))
def endpoint():
    return layab.created_response("/this_is_the_location")
```

Layab 2.*

```python
import layab

def endpoint(request):
    """
    responses:
        201:
            description: "Resource created"
            headers:
                location:
                    description: "Resource location."
                    type: string
            schema:
                type: string
    """
    return layab.LocationResponse(request, "/this_is_the_location")
```

### Updated response

Layab 1.*

```python
import layab

api = None

@api.doc(**layab.updated_response_doc(api))
def endpoint():
    return layab.updated_response("/this_is_the_location")
```

Layab 2.*

```python
import layab

def endpoint(request):
    """
    responses:
        201:
            description: "Resource updated"
            headers:
                location:
                    description: "Resource location."
                    type: string
            schema:
                type: string
    """
    return layab.LocationResponse(request, "/this_is_the_location")
```

### Deleted response

Layab 1.*

```python
import layab

api = None

@api.response(*layab.deleted_response_doc)
def endpoint():
    return layab.deleted_response
```

Layab 2.*

```python
from starlette.responses import Response

def endpoint(request):
    """
    responses:
        204:
            description: "Resource deleted"
    """
    return Response(status_code=204)
```

## How to install
1. [python 3.6+](https://www.python.org/downloads/) must be installed
2. Use pip to install module:
```sh
python -m pip install layab
```
