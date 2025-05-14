local utils = import 'utils.libjsonnet';

(import 'defaults.libjsonnet') + {
  // Project-specific
  description: 'Simple tracking of your home directory with easy-to-read diffs.',
  keywords: ['command line', 'file management', 'git', 'version control'],
  project_name: 'baldwin',
  version: '0.0.8',
  want_main: true,
  citation+: {
    'date-released': '2025-04-12',
  },
  pyproject+: {
    project+: {
      scripts: {
        bw: 'baldwin.main:baldwin',
        hgit: 'baldwin.main:git',
      },
    },
    tool+: {
      poetry+: {
        dependencies+: {
          binaryornot: '^0.4.4',
          click: '^8.1.8',
          gitpython: '^3.1.44',
          platformdirs: '^4.3.6',
          tomlkit: '^0.13.2',
        },
        group+: {
          dev+: {
            dependencies+: {
              'binaryornot-stubs': '^0',
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
  github+: {
    funding+: {
      ko_fi: funding_name,
      liberapay: funding_name,
      patreon: funding_name,
    },
  },
}
