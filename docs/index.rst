Baldwin
=======

.. only:: html

   .. image:: https://img.shields.io/pypi/pyversions/baldwin.svg?color=blue&logo=python&logoColor=white
      :target: https://www.python.org/
      :alt: Python versions

   .. image:: https://img.shields.io/pypi/v/baldwin
      :target: https://pypi.org/project/baldwin/
      :alt: PyPI - Version

   .. image:: https://img.shields.io/github/v/tag/Tatsh/baldwin
      :target: https://github.com/Tatsh/baldwin/tags
      :alt: GitHub tag

   .. image:: https://img.shields.io/github/license/Tatsh/baldwin
      :target: https://github.com/Tatsh/baldwin/blob/master/LICENSE.txt
      :alt: License

   .. image:: https://img.shields.io/github/commits-since/Tatsh/baldwin/v0.0.9/master
      :target: https://github.com/Tatsh/baldwin/compare/v0.0.9...master
      :alt: Commits since latest release

   .. image:: https://github.com/Tatsh/baldwin/actions/workflows/qa.yml/badge.svg
      :target: https://github.com/Tatsh/baldwin/actions/workflows/qa.yml
      :alt: QA

   .. image:: https://github.com/Tatsh/baldwin/actions/workflows/tests.yml/badge.svg
      :target: https://github.com/Tatsh/baldwin/actions/workflows/tests.yml
      :alt: Tests

   .. image:: https://coveralls.io/repos/github/Tatsh/baldwin/badge.svg?branch=master
      :target: https://coveralls.io/github/Tatsh/baldwin?branch=master
      :alt: Coverage Status

   .. image:: https://readthedocs.org/projects/baldwin/badge/?version=latest
      :target: https://baldwin.readthedocs.org/?badge=latest
      :alt: Documentation Status

   .. image:: https://www.mypy-lang.org/static/mypy_badge.svg
      :target: http://mypy-lang.org/
      :alt: mypy

   .. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
      :target: https://github.com/pre-commit/pre-commit
      :alt: pre-commit

   .. image:: https://img.shields.io/badge/pydocstyle-enabled-AD4CD3
      :target: http://www.pydocstyle.org/en/stable/
      :alt: pydocstyle

   .. image:: https://img.shields.io/badge/pytest-zz?logo=Pytest&labelColor=black&color=black
      :target: https://docs.pytest.org/en/stable/
      :alt: pytest

   .. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
      :target: https://github.com/astral-sh/ruff
      :alt: Ruff

   .. image:: https://static.pepy.tech/badge/baldwin/month
      :target: https://pepy.tech/project/baldwin
      :alt: Downloads

   .. image:: https://img.shields.io/github/stars/Tatsh/baldwin?logo=github&style=flat
      :target: https://github.com/Tatsh/baldwin/stargazers
      :alt: Stargazers

   .. image:: https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fpublic.api.bsky.app%2Fxrpc%2Fapp.bsky.actor.getProfile%2F%3Factor%3Ddid%3Aplc%3Auq42idtvuccnmtl57nsucz72%26query%3D%24.followersCount%26style%3Dsocial%26logo%3Dbluesky%26label%3DFollow%2520%40Tatsh&query=%24.followersCount&style=social&logo=bluesky&label=Follow%20%40Tatsh
      :target: https://bsky.app/profile/Tatsh.bsky.social
      :alt: Follow @Tatsh on Bluesky

   .. image:: https://img.shields.io/mastodon/follow/109370961877277568?domain=hostux.social&style=social
      :target: https://hostux.social/@Tatsh
      :alt: Mastodon Follow

This is a conversion of my simple scripts to version my home directory with very specific excludes
and formatting every file upon commit so that readable diffs can be generated.

Commands
--------

.. click:: baldwin.main:baldwin
  :prog: bw
  :nested: full

.. click:: baldwin.main:git
  :prog: hgit
  :nested: full

.. only:: html

   Library
   -------
   .. automodule:: baldwin
      :members:

   .. automodule:: baldwin.lib
      :members:

   .. automodule:: baldwin.typing
      :members:

   Indices and tables
   ==================

   * :ref:`genindex`
   * :ref:`modindex`
   * :ref:`search`
