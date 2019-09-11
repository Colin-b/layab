# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.2.0] - 2019-09-11
### Changed
- Health check now follow latest version of the Health Check RFC (draft version 3) meaning "details" key is now "checks".

## [1.1.1] - 2019-08-26
### Fixed
- Use werkzeug ProxyFix instead of a homemade one. It should fix the issue with serving OpenAPI definition to Swagger-UI using HTTPS.
- Remove bottom links from /changelog results

## [1.1.0] - 2019-08-21
### Changed
- Remove pre-commit from dependencies and add information on CONTRIBUTING guide on how to install it using pip.
- Update flask-restplus to version 0.13.0
- Update PyYAML to version 5.1.2

## [1.0.0] - 2019-08-01
### Changed
- Initial release.

[Unreleased]: https://github.tools.digital.engie.com/gempy/layab/compare/v1.2.0...HEAD
[1.2.0]: https://github.tools.digital.engie.com/gempy/layab/compare/v1.1.1...v1.2.0
[1.1.1]: https://github.tools.digital.engie.com/gempy/layab/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.tools.digital.engie.com/gempy/layab/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.tools.digital.engie.com/gempy/layab/releases/tag/v1.0.0
