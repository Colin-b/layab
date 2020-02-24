# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/Colin-b/layab/compare/v2.0.0...HEAD
[2.0.0]: https://github.com/Colin-b/layab/compare/v2.0.0a1...v2.0.0
[2.0.0a1]: https://github.com/Colin-b/layab/compare/v1.5.0...v2.0.0a1
[1.6.0]: https://github.com/Colin-b/layab/compare/v1.5.0...v1.6.0
[1.5.0]: https://github.com/Colin-b/layab/compare/v1.4.0...v1.5.0
[1.4.0]: https://github.com/Colin-b/layab/releases/tag/v1.4.0
