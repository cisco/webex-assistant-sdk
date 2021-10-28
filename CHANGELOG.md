# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 2.0.8 - 2021-10-28

### Changed

- Simplified README and pointed to official SDK resources.

## 1.0.0 - 2021-09-28

### Added

- Added key generation CLI command

### Changed

- Prior key generation methods output keys in the OpenSSH format. The decision was made to only support the PEM
  encoding format for skill keys going forward. As such the CLI now outputs RSA keys in a PEM format.
- Examples and tests have been updated to reflect that key format change.
- The SkillApplication class has been removed from the top level package and must now be imported from the app module.
- The __main__ file has been removed for now and the cli is now contained in the cli module.


## 0.5.0 - 2021-09-10

### Changed

- Updated SDK to use new encryption methodology on new `Skills Service`
- Needs to pass a private key when creating a `SkillApplication`

## 0.4.0 - 2021-08-19

### Changed

- Removed custom token formats for payload encryption in favor of HTTPS
- Removed `generate-key` command from cli

## 0.3.0 - 2021-07-20

### Added

- Implemented `new` CLI command
- Implemented `assistant-event` directive

### Changed

- Changed the unsupported `go-home` for the new `dismiss-web-view` directive

### Fixed

- Fixed key password validation

## 0.2.0 - 2021-02-09

### Added

- Added a check to skill server implementation
- Added `wxa_sdk check` command-line command to invoke a skill's health check
- Added this changelog

### Changed

- Changed response serialization in server to be compatible with mindmeld 4.3.4

## 0.1.1 - 2020-02-19

- Initial implementation
