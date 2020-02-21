<h2 align="center">Layab: Wonderful REST API</h2>

<p align="center">
<a href="https://pypi.org/project/layab/"><img alt="pypi version" src="https://img.shields.io/pypi/v/layab"></a>
<a href="https://travis-ci.com/Colin-b/layab"><img alt="Build status" src="https://api.travis-ci.com/Colin-b/layab.svg?branch=master"></a>
<a href="https://travis-ci.com/Colin-b/layab"><img alt="Coverage" src="https://img.shields.io/badge/coverage-100%25-brightgreen"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://travis-ci.com/Colin-b/layab"><img alt="Number of tests" src="https://img.shields.io/badge/tests-30 passed-blue"></a>
<a href="https://pypi.org/project/layab/"><img alt="Number of downloads" src="https://img.shields.io/pypi/dm/layab"></a>
</p>

> This is an alpha version for the version 2 of layab.
> Use with caution as it might still change.

Layab stands for `Wonderful` in Somali and is also a shortcut for `Layabout` (aren't we all lazy).

This package provides helper functions on top of [Starlette](https://www.starlette.io).

If you were using layab 1.* (based on [Flask-RestPlus](https://github.com/noirbizarre/flask-restplus), a project that is now dead and will not be compatible starting with Python 3.9), please refer to the [Migration guide](#migration-guide).

We learned the heard way not to use a full featured framework such as Flask-RestPlus, this is why, starting with layab 2, focus will be on modularity,

However, if you still want to use an all-in-one framework, you can still use layab 2 with any of the Starlette based framework that are currently surrounded with hype such as FastAPI or Responder.

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

If an information on something that was previously existing is missing, please open an issue.

### Create application and OpenAPI definition and Swagger-UI endpoints

Layab 1.*

```python
import layab

app, api = layab.create_api(
    __file__,
    compress_mimetypes=["text/csv", "application/json"],
    title="My API.",
    description="My description.",
)
```

Layab 2.*

```python
import layab
from starlette.applications import Starlette
import apispec_starlette

app = Starlette(middleware=layab.middleware())
spec = apispec_starlette.add_swagger_json_endpoint(
    app, 
    title="My API.",
    version="1.0.0",  # You now have to set the version yourself
    info={
        "description": "My description.",
        "x-server-environment": layab.get_environment(),
    }
)
# You will however lose the Swagger-ui that was available on / (root endpoint)
# We advise to install it on your Docker image first and then serve the directory as "/" as the last declared route.
```

### Monitoring endpoints

Layab 1.*

```python
import layab

api = None

def health_details():
    pass  # Implement this


layab.add_monitoring_namespace(api, health_details)
```

Layab 2.*

```python
import os.path

from starlette.applications import Starlette
from healthpy.starlette import add_consul_health_endpoint
from keepachangelog.starlette import add_changelog_endpoint

app = Starlette()

def health_check():
    pass  # Implement this


add_consul_health_endpoint(app, health_check)
# You now have to set the path to the changelog yourself
changelog_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "CHANGELOG.md")
add_changelog_endpoint(app, changelog_path)
```

You can now add only one of the two initially provided endpoints (in case you don't have or want to expose your changes).

Refer to [healthpy](https://pypi.org/project/healthpy/) documentation for more information on what is possible to check API health.

Refer to [keepachangelog](https://pypi.org/project/keepachangelog/) documentation for more information on how changelog is handled.

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
