# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.2.0] - 2020-10-09
### Added
- flask_restx request logging now log processing_time in case of failure as well.
- Explicit support for python 3.9

### Changed
- Only store one request id per query.
- flask_restx request logging now log request details as a dictionary linked to request key.
- flask_restx request logging now log request arguments as a dictionary linked to request.args key.
- flask_restx request logging now log request headers as a dictionary linked to request.headers key.
- flask_restx request logging now log request error as a dictionary linked to error key.
- flask_restx request logging now log status as `end` instead of `success` as it might be misleading if app is sending failure response.

### Fixed
- flask_restx request logging do not log request data in case of exception anymore as it might be too big or bytes could not be supported by the logger.
- flask_restx request logging now log all params as a list of values, only the first value for each param was logged previously.

## [2.1.0] - 2020-09-30
### Added
- Add support for `flask-restx` framework.

### Changed
- Update [`black`](https://pypi.org/project/black/) version from `master` to `20.8b1`.

## [2.0.0] - 2020-02-24
### Changed
- [Starlette](https://www.starlette.io) is now an optional dependency and everything related to it is now within layab.starlette module.

## [2.0.0a1] - 2020-02-21
### Changed
- Switch from Flask-RestPlus to [Starlette](https://www.starlette.io).

## [1.6.0] - 2020-01-15
### Added
- Log request upon receipt.
- Add request_status to logging to know what a log is for.
- Add request_status_code to logging to know the actual HTTP status code sent as response.
- Avoid duplicated logging when used as a decorator.

## [1.5.0] - 2019-12-03
### Added
- Allow to load unsafe logging configuration files, see [PyYAML](https://pyyaml.org/wiki/PyYAMLDocumentation) documentation for more information on unsafe YAML loading.

## [1.4.0] - 2019-11-29
### Added
- Initial release.

[Unreleased]: https://github.com/Colin-b/layab/compare/v2.2.0...HEAD
[2.2.0]: https://github.com/Colin-b/layab/compare/v2.1.0...v2.2.0
[2.1.0]: https://github.com/Colin-b/layab/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/Colin-b/layab/compare/v2.0.0a1...v2.0.0
[2.0.0a1]: https://github.com/Colin-b/layab/compare/v1.5.0...v2.0.0a1
[1.6.0]: https://github.com/Colin-b/layab/compare/v1.5.0...v1.6.0
[1.5.0]: https://github.com/Colin-b/layab/compare/v1.4.0...v1.5.0
[1.4.0]: https://github.com/Colin-b/layab/releases/tag/v1.4.0
