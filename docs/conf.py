"""See https://www.sphinx-doc.org/en/master/usage/configuration.html."""
from datetime import UTC, datetime
from operator import itemgetter
from pathlib import Path
import sys

import tomlkit

with (Path(__file__).parent.parent / 'pyproject.toml').open() as f:
    content = tomlkit.load(f).unwrap()
    authors, name, version = itemgetter('authors', 'name', 'version')(content['project'])
    poetry = content['tool']['poetry']
# region Path setup
# If extensions (or modules to document with autodoc) are in another directory, add these
# directories to sys.path here. If the directory is relative to the documentation root, use
# str(Path().parent.parent) to make it absolute, like shown here.
sys.path.insert(0, str(Path(__file__).parent.parent))
# endregion
author = f'{authors[0]["name"]} <f{authors[0]["email"]}>'
copyright = str(datetime.now(UTC).year)  # noqa: A001
project = name
release = f'v{version}'
extensions = ('sphinx.ext.autodoc', 'sphinx.ext.intersphinx', 'sphinx.ext.napoleon',
              'sphinx.ext.viewcode', *(('sphinx_click',) if poetry.get('scripts') else ()))
html_theme = 'sphinxdoc'
templates_path = ['_templates']

datatables_class = 'sphinx-datatable'
datatables_options = {'paging': 0}
datatables_version = '1.13.4'
intersphinx_mapping = {
    'gitpython': ('https://gitpython.readthedocs.io/en/stable/', None),
    'python': ('https://docs.python.org/3.13', None),
    'tomlkit': ('https://tomlkit.readthedocs.io/en/latest/', None)
}
intersphinx_cache_limit = 0
viewcode_line_numbers = True
