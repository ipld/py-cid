# News Fragments

This directory contains news fragments for [towncrier](https://github.com/twisted/towncrier).

## How to add a news fragment

1. Create a new file in this directory with the naming pattern: `{issue_number}.{type}.rst`

1. The `{type}` should be one of:

   - `breaking` - Breaking changes
   - `bugfix` - Bug fixes
   - `deprecation` - Deprecations
   - `docs` - Documentation improvements
   - `feature` - New features
   - `internal` - Internal changes for contributors
   - `misc` - Miscellaneous changes
   - `performance` - Performance improvements
   - `removal` - Removed features

1. The content should be a brief description of the change, written in rst format.

## Examples

- `123.feature.rst` - New feature for issue #123
- `456.bugfix.rst` - Bug fix for issue #456
- `789.internal.rst` - Internal change for issue #789

## Generating the changelog

When releasing a new version, run:

```bash
towncrier --version 0.4.0
```

This will:

- Read all news fragments
- Generate a structured changelog in `HISTORY.rst`
- Delete the fragment files
