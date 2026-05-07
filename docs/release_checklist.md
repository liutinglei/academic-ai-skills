# Release Checklist

Use this checklist before publishing a release or announcing the repository.

## Repository Hygiene

- [ ] `_reference/` is ignored and absent from tracked files.
- [ ] Examples contain only synthetic, public, or non-confidential material.
- [ ] The README status table matches the actual skill state.
- [ ] License and attribution notes are present.

## Skill Quality

- [ ] Each `SKILL.md` has valid YAML frontmatter.
- [ ] Trigger descriptions mention concrete use cases.
- [ ] Instructions avoid copying third-party skill content.
- [ ] Integrity rules prohibit fabricated comments, references, data, line numbers, and manuscript changes.
- [ ] Templates are usable without requiring private manuscript material.

## Validation

- [ ] Run `python -m unittest discover -s tests`.
- [ ] Run the comment parser on `examples/reviewer-response-demo/sample_comments.txt`.
- [ ] Run skill validation on `skills/reviewer-response`.
