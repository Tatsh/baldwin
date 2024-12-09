# Simple home directory versioning

[![QA](https://github.com/Tatsh/baldwin/actions/workflows/qa.yml/badge.svg)](https://github.com/Tatsh/baldwin/actions/workflows/qa.yml)
[![Tests](https://github.com/Tatsh/baldwin/actions/workflows/tests.yml/badge.svg)](https://github.com/Tatsh/baldwin/actions/workflows/tests.yml)
[![Coverage Status](https://coveralls.io/repos/github/Tatsh/baldwin/badge.svg?branch=master)](https://coveralls.io/github/Tatsh/baldwin?branch=master)
[![Documentation Status](https://readthedocs.org/projects/baldwin/badge/?version=latest)](https://baldwin.readthedocs.io/en/latest/?badge=latest)
![PyPI - Version](https://img.shields.io/pypi/v/baldwin)
![GitHub tag (with filter)](https://img.shields.io/github/v/tag/Tatsh/baldwin)
![GitHub](https://img.shields.io/github/license/Tatsh/baldwin)
![GitHub commits since latest release (by SemVer including pre-releases)](https://img.shields.io/github/commits-since/Tatsh/baldwin/v0.0.5/master)

This is a conversion of my simple scripts to version my home directory with very specific excludes
and formatting every file upon commit so that readable diffs can be generated.

## Installation

```shell
pip install baldwin
```

## Usage

```plain
 $ bw -h
Usage: bw [OPTIONS] COMMAND [ARGS]...

  Manage a home directory with Git.

Options:
  -d, --debug  Enable debug logging.
  -h, --help   Show this message and exit.

Commands:
  auto-commit
  format
  git
  info
  init
  install-units
```

In addition to the `bw` command, `hgit` is a shortcut for `bw git`.

### Start a new repository

```shell
bw init
```

Find out where the Git directory is by running `bw info`. This can be done even if `init` has not
been run.

### Automation

#### systemd

```shell
bw install-units
```

This will install a timer that will automatically make a new commit every 6 hours. It does not push.

Keep in mind that systemd units require a full path to the executable, so you must keep the unit
up-to-date if you move where you install this package. Simply run `bw install-units` again.

Note that user systemd units only run while logged in.

To disable and remove the units, use the following commands:

```shell
systemctl disable --now home-vcs.timer
rm ~/.config/systemd/user/home-vcs.*
```

### Pushing

To push, use either of the following:

- `bw git push`
- `hgit push`

The above also demonstrates that `bw git`/`hgit` are just frontends to `git` with the correct
environment applied.

## Formatting

If Prettier is installed, it will be used to format files. The configuration used comes with this
package. Having consistent formatting allows for nice diffs to be generated.

If you have initialised a repository without having `prettier` or `jq` in `PATH`, you need to run the
following commands to enable readable diffs:

```shell
hgit config diff.json.textconv 'jq -MS .'
hgit config diff.json.cachetextconv true
hgit config diff.yaml.textconv 'prettier --no-editorconfig --parser yaml'
hgit config diff.yaml.cachetextconv true
```

If you have the XML plugin installed:

```shell
hgit config diff.xml.textconv 'prettier --no-editorconfig --parser xml --xml-whitespace-sensitivity ignore'
hgit config diff.xml.cachetextconv true
```

## Binary files

Any file that is untracked and detected to be binary will not be added. Use `hgit add` to add a
binary file manually.

## Other details

Default `.gitignore` and `.gitattributes` files are installed on initialisation. They are never
modified by this tool. Please customise as necessary.
