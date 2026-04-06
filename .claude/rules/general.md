# General guidelines

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

## Avoiding Permission Prompts

Bash commands containing `$()` subshells trigger interactive permission prompts. Avoid these:

- **Git commits**: create `.wiswa-ci` if it does not exist (`mkdir -p .wiswa-ci`), then create a
  unique message file with `mktemp .wiswa-ci/message-XXXXXXXX`. Write the commit message there with
  the **Write** tool (not Bash `echo` or `cat`). Commit with
  `git commit -S -s -F <tempfile>` without using the
  sandbox. Never use `-m "$(cat <<'EOF' ...)"` or write the message file from Bash with a
  fixed path (permission prompts).
- **Command substitution**: prefer chaining with `&&` and temp files over `$()` inline.
- **Backticks**: same issue as `$()` - avoid `` `command` `` in Bash tool calls.
- **Pipes into commands** are fine (`echo foo | git commit --stdin` etc.).
