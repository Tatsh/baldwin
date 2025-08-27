local utils = import 'utils.libjsonnet';

(import 'defaults.libjsonnet') + {
  // Project-specific
  description: 'Simple tracking of your home directory with easy-to-read diffs.',
  keywords: ['command line', 'file management', 'git', 'version control'],
  project_name: 'baldwin',
  version: '0.0.9',
  want_main: true,
  citation+: {
    'date-released': '2025-08-27',
  },
  copilot: {
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
          binaryornot: '^0.4.4',
          gitpython: '^3.1.45',
          platformdirs: '^4.4.0',
          tomlkit: '^0.13.3',
        },
        group+: {
          dev+: {
            dependencies+: {
              'types-binaryornot': '^0.4.0.20250507',
            },
          },
        },
      },
    },
  },
  // Common
  authors: [
    {
      'family-names': 'Udvare',
      'given-names': 'Andrew',
      email: 'audvare@gmail.com',
      name: '%s %s' % [self['given-names'], self['family-names']],
    },
  ],
  local funding_name = '%s2' % std.asciiLower(self.github_username),
  github_username: 'Tatsh',
  social+: {
    mastodon+: { id: '109370961877277568' },
  },
  github+: {
    funding+: {
      ko_fi: funding_name,
      liberapay: funding_name,
      patreon: funding_name,
    },
  },
}
