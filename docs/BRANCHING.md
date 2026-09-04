# Branching Strategy

This repository uses a lightweight category-integration branching model.

## Branch roles

- `main` — stable, usable scripts and documentation.
- Category branches such as `email` — integration branches for related utilities.
- Short-lived feature branches such as `feat/gmail-retention-cleaner` — isolated development for a specific utility or substantial change.

## Workflow

1. Start a feature branch from the relevant category branch.
2. Develop and test the utility on the feature branch.
3. Open a pull request from the feature branch into the category branch.
4. Merge tested category work into `main` periodically.
5. Delete completed feature branches after merge.

Example:

```text
main
  └── email
        ├── feat/gmail-retention-cleaner
        ├── feat/attachment-mail-merge
        └── feat/daily-inbox-digest
```

## Categories

Categories are represented primarily by folders in the repository. Create a category branch only when there is active work in that category; do not create empty branches pre-emptively.

Current and anticipated categories include:

- `email/`
- `microsoft-365/`
- `system/`
- `networking/`
- `data/`
- `files/`
- `automation/`
- `web/`
- `utilities/`

## Naming

Feature branches should use concise names such as:

```text
feat/gmail-retention-cleaner
feat/attachment-mail-merge
fix/outlook-bulk-mail-auth
refactor/email-common-config
```

Category branches should use the category name directly, for example `email` or `networking`.
