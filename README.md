<h2 align="center">Layab: Wonderful REST API</h2>

<p align="center">
<a href='https://github.tools.digital.engie.com/gempy/layab/releases/latest'><img src='https://pse.tools.digital.engie.com/drm-all.gem/buildStatus/icon?job=team/layab/master&config=version'></a>
<a href='https://pse.tools.digital.engie.com/drm-all.gem/job/team/view/Python%20modules/job/layab/job/master/'><img src='https://pse.tools.digital.engie.com/drm-all.gem/buildStatus/icon?job=team/layab/master'></a>
<a href='https://pse.tools.digital.engie.com/drm-all.gem/job/team/view/Python%20modules/job/layab/job/master/cobertura/'><img src='https://pse.tools.digital.engie.com/drm-all.gem/buildStatus/icon?job=team/layab/master&config=testCoverage'></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href='https://pse.tools.digital.engie.com/drm-all.gem/job/team/view/Python%20modules/job/layab/job/master/lastSuccessfulBuild/testReport/'><img src='https://pse.tools.digital.engie.com/drm-all.gem/buildStatus/icon?job=team/layab/master&config=testCount'></a>
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

## Flask RestPlus ##

The way your REST API behaves can be standardized

### Default behavior ###

Importing layab will make sure that every flask request is logged on reception. 

```python
import layab
```

## How to install
1. [python 3.7+](https://www.python.org/downloads/) must be installed
2. Use pip to install module:
```sh
python -m pip install layab -i https://all-team-remote:tBa%40W%29tvB%5E%3C%3B2Jm3@artifactory.tools.digital.engie.com/artifactory/api/pypi/all-team-pypi-prod/simple
```
