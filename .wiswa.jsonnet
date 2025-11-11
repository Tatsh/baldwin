local utils = import 'utils.libjsonnet';

{
  description: 'Simple tracking of your home directory with easy-to-read diffs.',
  keywords: ['command line', 'file management', 'git', 'version control'],
  project_name: 'baldwin',
  version: '0.0.10',
  want_main: true,
  copilot+: {
    intro: 'Baldwin is a command line tool for tracking a home directory with Git.',
  },
  docs_conf+: {
    config+: {
      intersphinx_mapping+: {
        binaryornot: ['https://binaryornot.readthedocs.io/en/latest/', null],
        click: ['https://click.palletsprojects.com/en/latest/', null],
        gitpython: ['https://gitpython.readthedocs.io/en/stable/', null],
        platformdirs: ['https://platformdirs.readthedocs.io/en/latest/', null],
        tomlkit: ['https://tomlkit.readthedocs.io/en/latest/', null],
        'typing-extensions': ['https://typing-extensions.readthedocs.io/en/latest/', null],
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
}
