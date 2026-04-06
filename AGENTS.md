# Agents and AI guidance

All agent definitions, skills, and project rules live under **`.claude/`**. Use that tree whether you
use Claude Code, Cursor, GitHub Copilot, or another assistant: open or reference the files directly,
and use each product's own mechanics for attaching repo context where needed.

- **Hard prerequisite before any repository edit:** Read [.claude/rules/general.md](.claude/rules/general.md)
  in full (including _Before editing repository files_), then every other relevant
  `.claude/rules/*.md` for the paths you will change, and any applicable `.claude/agents/*.md` or
  `.claude/skills/*/SKILL.md` (for example when the task follows CI, regen, or another named
  workflow, or the user names an agent or skill). Do this **before** creating, modifying, or deleting
  tracked files.
- If the user is only adding instructions for the assistant, **do not edit the repository** unless
  they ask for a concrete change.

## General conventions

These match [.claude/rules/general.md](.claude/rules/general.md).

- Do not explain project structure or conventions in comments or docstrings.
- Use 2 spaces for indentation except in Python.
- Files must end with a single newline character.
- Keep lines shorter than 100 characters.
- Line endings must be Unix-style (LF).
- Use UTF-8 encoding for all files.
- Use spaces instead of tabs for indentation.
- Use British spelling in comments and docstrings.
- Use American spelling for all identifiers and string literals.
- Never mention the spelling or other project conventions in comments or docstrings.
- Use full sentences in comments and docstrings.
- Use the Oxford comma in lists.
- Use single quotes for strings, except where double quotes are required (e.g., JSON).
- Full words should be preferred over abbreviations, except for well-known acronyms. Some words may
  be abbreviated:
  - `config` for configuration.
- Prefer to use immutable data structures over mutable ones.
- Run `yarn format` after any changes to format all files. Must exit with code 0.
- Run `yarn qa` after any changes to type-check and run QA utilities. Must exit with code 0. Both
  commands must pass before committing.
- Use `yarn` to invoke Node-based tools (Prettier, markdownlint-cli2, cspell).
- Use `uv run` to invoke Python tools (pytest, mypy, Ruff).
- Spell-check uses cspell with British English (`en-GB`). Exception: code identifiers must use
  American English (`ColorCode` not `ColourCode`).
- Add new words to `.vscode/dictionary.txt` in lowercase and keep the file sorted. Prefer to commit
  dictionary changes separately with the message `dictionary: update`.

## Rules (`.claude/rules/`)

| File                                          | Scope                                 |
| --------------------------------------------- | ------------------------------------- |
| [general](.claude/rules/general.md)           | Project-wide conventions              |
| [python](.claude/rules/python.md)             | Python coding (`**/*.py`, `**/*.pyi`) |
| [python-tests](.claude/rules/python-tests.md) | Test conventions (`tests/**/*.py`)    |
| [json-yaml](.claude/rules/json-yaml.md)       | JSON and YAML files                   |
| [toml-ini](.claude/rules/toml-ini.md)         | TOML and INI files                    |
| [markdown](.claude/rules/markdown.md)         | Markdown files                        |

## Skills (`.claude/skills/`)

Skills are folders with a `SKILL.md` file (for example [ci](.claude/skills/ci/SKILL.md) when
present).

## Agents (`.claude/agents/`)

| Agent                                                        | Purpose                                                    |
| ------------------------------------------------------------ | ---------------------------------------------------------- |
| [python-expert](.claude/agents/python-expert.md)             | General expert-level Python coding (includes mypy/typing)  |
| [mypy-fixer](.claude/agents/mypy-fixer.md)                   | Fix mypy errors and eliminate `Any`                        |
| [python-moderniser](.claude/agents/python-moderniser.md)     | Upgrade code to modern Python features                     |
| [docstring-fixer](.claude/agents/docstring-fixer.md)         | Audit and fix missing/incomplete docstrings                |
| [test-writer](.claude/agents/test-writer.md)                 | Generate tests following project patterns                  |
| [coverage-improver](.claude/agents/coverage-improver.md)     | Identify coverage gaps and write tests                     |
| [click-auditor](.claude/agents/click-auditor.md)             | Validate Click command consistency                         |
| [markdownlint-fixer](.claude/agents/markdownlint-fixer.md)   | Fix markdownlint-cli2 issues                               |
| [qa-fixer](.claude/agents/qa-fixer.md)                       | Run `yarn format` and `yarn qa` until clean                |
| [workflow-shellcheck](.claude/agents/workflow-shellcheck.md) | ShellCheck embedded Bash in workflow YAML                  |
| [copy-editor](.claude/agents/copy-editor.md)                 | Fix prose style, grammar, and spelling in comments/strings |
| [badge-sync](.claude/agents/badge-sync.md)                   | Sync `docs/badges.rst` with `README.md`                    |
| [changelog](.claude/agents/changelog.md)                     | Update CHANGELOG.md with entries since last release        |
| [regen](.claude/agents/regen.md)                             | Run Wiswa, post-process, verify, and commit                |
| [release](.claude/agents/release.md)                         | Changelog, version bump, push                              |
| [wiswa-sync](.claude/agents/wiswa-sync.md)                   | Reflect managed file changes back to `.wiswa.jsonnet`      |
