# Contributing

Thanks for looking. This repo is one person's working setup, kept in public, so the most useful contributions are bug reports, experiment ideas and small fixes.

## Ways to help

- **Report a bug** with the [bug template](.github/ISSUE_TEMPLATE/bug.md): a skill that misfires, a hook that blocks when it should not, a broken link.
- **Suggest an experiment** with the [experiment idea template](.github/ISSUE_TEMPLATE/experiment-idea.md). It asks for the same fields as a [lab entry](lab/README.md).
- **Send a pull request** for a fix. For anything larger, open an issue first so we can agree on the shape.

## Rules for changes

- **No invented numbers.** Any number in a README, skill or lab entry needs a source: a command anyone can re-run, or a named, dated measurement. If you cannot source it, leave the number out.
- **Product-anonymous and private-free.** No personal paths, email addresses, internal IDs, chat links or company names. The privacy lint checks for the generic patterns.
- **Portable skills.** `SKILL.md` frontmatter uses only `name`, `description`, `license`, `compatibility`, `metadata` and `allowed-tools`. `name` matches the folder. `description` starts with "Use when", lists triggers rather than the workflow, and stays under 1,536 characters.
- **Hooks fail open.** On any error or unexpected input, a hook exits 0 with no output. Reference plugin files through `${CLAUDE_PLUGIN_ROOT}` and run Python with `python3 -I`.
- **Markdown is the tested backend.** Other backends go in a `references/` file marked untested.
- **A bug fix ships with a regression test** that fails before the fix and passes after.
- **Lab entries are append-only.** Use the template in [lab/README.md](lab/README.md). Write an unmeasured result as "pending". Do not predict it.

## Checks

Run these from the repo root before opening a pull request. Each must exit 0.

```
python3 -m unittest discover -s tests
python3 -m unittest discover -s plugins/proof-before-done/tests
python3 -m unittest discover -s plugins/operating-rules/tests
bash tests/test_privacy_lint.sh
python3 scripts/check_skills.py
python3 scripts/check_links.py
bash scripts/privacy-lint.sh
claude plugin validate . --strict
```

## Commits

Use conventional commit prefixes, scoped to the plugin when there is one: `feat(pm-routines): ...`, `fix(proof-before-done): ...`, `docs: ...`. Add a line to [CHANGELOG.md](CHANGELOG.md) for anything a user would notice.

## License

By contributing, you agree that your contribution is licensed under the [MIT License](LICENSE).
