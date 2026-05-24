# Roadmap

`dotpath`: Dotted-key get/set/has/del over nested dicts and lists, like jq's path syntax minus the language. Zero dependencies..

## Near Term

- Keep the README specific: audience, thesis, quick demo, limitations, and
  source-checkout install instructions.
- Keep edge-case tests near the code they protect.
- Keep CI aligned with the local commands: `pytest` and `python -m build` where
  applicable.

## Release Readiness

- Verify package metadata before publishing anywhere.
- Add a release tag only after tests, type checks, build/pack checks, and docs
  are all current.
- Do not add download, usage, benchmark, or adoption claims without evidence.

## Later

- Add small examples for the most common workflow.
- Add benchmark or conformance scripts only where performance or standards
  compliance is part of the value proposition.
- Consolidate with a sibling repo if the audience and API overlap too much.
