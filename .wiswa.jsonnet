local utils = import 'utils.libjsonnet';

{
  uses_user_defaults: true,
  description: 'Simple tracking of your home directory with easy-to-read diffs.',
  keywords: ['command line', 'file management', 'git', 'version control'],
  project_name: 'baldwin',
  version: '0.0.10',
  want_main: true,
  want_flatpak: true,
  publishing+: { flathub: 'sh.tat.baldwin' },
  pyinstaller+: {
    collect_data: ['binaryornot'],
  },
  docs_conf+: {
    config+: {
      intersphinx_mapping+: {
        anyio: ['https://anyio.readthedocs.io/en/stable/', null],
        binaryornot: ['https://binaryornot.readthedocs.io/en/latest/', null],
        click: ['https://click.palletsprojects.com/en/latest/', null],
        gitpython: ['https://gitpython.readthedocs.io/en/stable/', null],
        platformdirs: ['https://platformdirs.readthedocs.io/en/latest/', null],
        tomlkit: ['https://tomlkit.readthedocs.io/en/latest/', null],
        'typing-extensions': ['https://typing-extensions.readthedocs.io/en/latest/', null],
      },
    },
  },
  snapcraft+: {
    apps+: {
      baldwin+: {
        command: 'bin/bw',
      },
    },
  },
  pyproject+: {
    project+: {
      scripts: {
        bw: 'baldwin.main:baldwin',
        hgit: 'baldwin.main:git',
      },
    },
    tool+: {
      coverage+: {
        report+: { omit+: ['baldwin/typing.py'] },
        run+: { omit+: ['baldwin/typing.py'] },
      },
      poetry+: {
        dependencies+: {
          anyio: utils.latestPypiPackageVersionCaret('anyio'),
          binaryornot: utils.latestPypiPackageVersionCaret('binaryornot'),
          gitpython: utils.latestPypiPackageVersionCaret('gitpython'),
          platformdirs: utils.latestPypiPackageVersionCaret('platformdirs'),
          tomlkit: utils.latestPypiPackageVersionCaret('tomlkit'),
        },
        group+: {
          dev+: {
            dependencies+: {
              'types-binaryornot': utils.latestPypiPackageVersionCaret('types-binaryornot'),
            },
          },
        },
      },
    },
  },
  flatpak+: {
    command: 'bw',
  },
}
