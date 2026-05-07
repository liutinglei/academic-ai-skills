# Academic AI Skills

Reusable AI-agent skills for systematic reviews, manuscript revision, reviewer response preparation, journal submission checks, and thesis correction auditing.

This project is for researchers, PhD students, journal authors, and academic writers who use AI coding agents such as Claude Code, Codex, or other LLM-based tools to make scholarly workflows more structured, auditable, and reproducible.

## Current Skills

| Skill | Purpose | Status |
|---|---|---|
| `reviewer-response` | Prepare and audit reviewer response letters, editor letters, and revision maps | v0.1.0 draft |
| `systematic-literature-review` | Support PRISMA-oriented systematic literature review workflows | Planned |
| `manuscript-audit` | Check consistency between claims, results, discussion, and conclusions | Planned |
| `journal-submission-checker` | Prepare journal submission packages and compliance checks | Planned |

## Why This Project Exists

Academic AI workflows need transparency, accuracy, ethical safeguards, and human judgment. This project focuses on reusable skills that help researchers:

- structure complex academic tasks
- avoid fabricated references or unsupported claims
- prepare transparent reviewer responses
- maintain revision traceability
- improve reproducibility in scholarly workflows

## Repository Structure

```text
academic-ai-skills/
+-- skills/
|   +-- reviewer-response/
|   |   +-- SKILL.md
|   |   +-- templates/
|   |   +-- scripts/
|   +-- systematic-literature-review/
+-- docs/
+-- examples/
+-- tests/
+-- _reference/      # ignored; local structural references only
```

## First Skill: Reviewer Response

The first skill is `reviewer-response`. It supports:

- editor cover letters
- reviewer-by-reviewer responses
- thesis examiner responses
- revision maps
- change logs
- consistency audits
- overclaiming checks

Example prompt:

```text
Use the reviewer-response skill to turn these reviewer comments into a response table. Mark any manuscript locations as [Author to verify].
```

Run the plain-text comment parser:

```bash
python skills/reviewer-response/scripts/comment_parser.py examples/reviewer-response-demo/sample_comments.txt
```

Output JSON for downstream processing:

```bash
python skills/reviewer-response/scripts/comment_parser.py examples/reviewer-response-demo/sample_comments.txt --json
```

Run tests:

```bash
python -m unittest discover -s tests
```

## Design Principles

- Human-in-the-loop academic judgment
- No fabricated references
- No fake data or unsupported statistical claims
- No confidential manuscript leakage in examples
- Transparent revision records
- Conservative and verifiable academic claims

See `docs/design_principles.md` and `docs/reference_audit.md` for project rules.

## Public Release Checklist

Before tagging a release:

- run the parser on the example comments
- run the test suite
- verify that `_reference/` is ignored
- confirm that examples contain only synthetic or public-safe content
- update the skill status table

## License

This project is released under the MIT License.
