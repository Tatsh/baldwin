from collections.abc import Iterable
from importlib import resources
from itertools import chain
from pathlib import Path
from shlex import quote
from shutil import which
import logging
import subprocess as sp

from git import Repo
import platformdirs

__all__ = ('format_', 'get_git_path', 'get_repo')

log = logging.getLogger(__name__)


def get_git_path() -> Path:
    """
    Get the Git directory (``GIT_DIR``).

    This path is platform-specific. On Windows, the Roaming AppData directory will be used.
    """
    return platformdirs.user_data_path('home-git', roaming=True)


def get_repo() -> Repo:
    """
    Get a :py:class:`git.Repo` object.

    Also disables GPG signing for the repository.
    """
    repo = Repo(get_git_path(), expand_vars=False)
    repo.git.execute(('git', 'config', 'commit.gpgsign', 'false'))
    return repo


def format_(filenames: Iterable[Path | str], log_level: str = 'error') -> None:
    """
    Format untracked and modified files in the repository.

    Does nothing if Prettier is not in ``PATH``.

    The following plugins will be detected and enabled if found:

    * @prettier/plugin-xml
    * prettier-plugin-ini
    * prettier-plugin-sort-json
    * prettier-plugin-toml
    """
    if not (filenames := list(filenames)):
        return
    with resources.path('baldwin.resources', 'prettier.config.json') as config_file:
        if not (prettier := which('prettier')):
            return
        # Detect plugins
        node_modules_path = (Path(prettier).resolve(strict=True).parent / '..' /
                             '..').resolve(strict=True)
        cmd = ('prettier', '--config', str(config_file), '--write',
               '--no-error-on-unmatched-pattern', '--ignore-unknown', '--log-level', log_level,
               *chain(*(('--plugin', str(fp)) for module in (
                   '@prettier/plugin-xml/src/plugin.js', 'prettier-plugin-ini/src/plugin.js',
                   'prettier-plugin-sort-json/dist/index.js', 'prettier-plugin-toml/lib/index.cjs')
                        if (fp := (node_modules_path / module)).exists())), *(str(x)
                                                                              for x in filenames))
        log.debug('Running: %s', ' '.join(quote(x) for x in cmd))
        sp.run(cmd, check=True)
