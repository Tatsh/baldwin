<!-- markdownlint-disable MD024 -->

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.1/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- `bw format` and `bw auto-commit` now run Prettier invocations and filesystem checks
  concurrently, bounded by the number of available CPUs, significantly reducing wall-clock time
  on repositories with many files.
- `-d`/`--debug` moved from the `bw` group to each subcommand (including `hgit`). Invocations
  like `bw -d auto-commit` must now be written as `bw auto-commit -d`.

### Fixed

- Snap app command now uses `bin/bw`, matching the console script installed by the part.

## [0.0.10]

### Changed

- Updated upper bound of Python version requirement.
- Updated all dependencies.
- Use trusted publishing.

## [0.0.9]

### Fixed

- auto-commit: do not try to add files that cannot be opened.

[unreleased]: https://github.com/Tatsh/baldwin/-/compare/v0.0.9...HEAD
[0.0.9]: https://github.com/Tatsh/baldwin/compare/v0.0.8...v0.0.9
