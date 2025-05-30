# Baldwin

[![Python versions](https://img.shields.io/pypi/pyversions/baldwin.svg?color=blue&logo=python&logoColor=white)](https://www.python.org/)
[![PyPI - Version](https://img.shields.io/pypi/v/baldwin)](https://pypi.org/project/baldwin/)
[![GitHub tag (with filter)](https://img.shields.io/github/v/tag/Tatsh/baldwin)](https://github.com/Tatsh/baldwin/tags)
[![License](https://img.shields.io/github/license/Tatsh/baldwin)](https://github.com/Tatsh/baldwin/blob/master/LICENSE.txt)
[![GitHub commits since latest release (by SemVer including pre-releases)](https://img.shields.io/github/commits-since/Tatsh/baldwin/v0.0.9/master)](https://github.com/Tatsh/baldwin/compare/v0.0.9...master)
[![QA](https://github.com/Tatsh/baldwin/actions/workflows/qa.yml/badge.svg)](https://github.com/Tatsh/baldwin/actions/workflows/qa.yml)
[![Tests](https://github.com/Tatsh/baldwin/actions/workflows/tests.yml/badge.svg)](https://github.com/Tatsh/baldwin/actions/workflows/tests.yml)
[![Coverage Status](https://coveralls.io/repos/github/Tatsh/baldwin/badge.svg?branch=master)](https://coveralls.io/github/Tatsh/baldwin?branch=master)
[![Documentation Status](https://readthedocs.org/projects/baldwin/badge/?version=latest)](https://baldwin.readthedocs.org/?badge=latest)
[![mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![pydocstyle](https://img.shields.io/badge/pydocstyle-enabled-AD4CD3)](http://www.pydocstyle.org/en/stable/)
[![pytest](https://img.shields.io/badge/pytest-zz?logo=Pytest&labelColor=black&color=black)](https://docs.pytest.org/en/stable/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Downloads](https://static.pepy.tech/badge/baldwin/month)](https://pepy.tech/project/baldwin)
[![Stargazers](https://img.shields.io/github/stars/Tatsh/baldwin?logo=github&style=flat)](https://github.com/Tatsh/baldwin/stargazers)

[![@Tatsh](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fpublic.api.bsky.app%2Fxrpc%2Fapp.bsky.actor.getProfile%2F%3Factor%3Ddid%3Aplc%3Auq42idtvuccnmtl57nsucz72%26query%3D%24.followersCount%26style%3Dsocial%26logo%3Dbluesky%26label%3DFollow%2520%40Tatsh&query=%24.followersCount&style=social&logo=bluesky&label=Follow%20%40Tatsh)](https://bsky.app/profile/Tatsh.bsky.social)

This is a conversion of my simple scripts to version my home directory with very specific excludes
and formatting every file upon commit so that readable diffs can be generated.

## Installation

### Pip

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
