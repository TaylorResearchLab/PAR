# Portable Assertion Records (PAR)

**Proposed specification v0.01**

Repository: https://github.com/TaylorResearchLab/PAR  
Draft editor and maintainer: Deanne M. Taylor

A Portable Assertion Record carries a scientific assertion with its claim boundary, defined identifiers, context and traceable provenance. Records can be extracted from existing resources, exchanged across data models and assembled into new knowledge graphs while retaining their origins.

Read [the specification](SPECIFICATION.md) for the proposed Core contract. [Open issues](OPEN_ISSUES.md) identify decisions still needed before the first approved release.

## Repository contents

- `SPECIFICATION.md`: proposed PAR Core, profiles, reconciliation and PAD release rules.
- `schemas/par-core-0.01.schema.json`: illustrative draft JSON envelope.
- `examples/`: fictional worked example and explanations.
- `CITATION.cff`: draft citation metadata, without an assigned DOI.
- `CHANGELOG.md`: specification history.
- `docs/RELEASE_CHECKLIST.md`: steps for a reviewable, citable release.

## Status

This is an initial framework proposal. The draft JSON profile is not yet a JKG implementation or an RDF/SHACL reference implementation. Source-aware validation and profile development accompany structural validation.

Release authorship and the licenses for documentation and software remain open decisions. This draft does not assign a license. Original scientific resources retain their own access and redistribution conditions.

## Citation

Proposed citation, pending author approval and archival release:

Taylor, Deanne M. *Portable Assertion Records (PAR): Proposed specification v0.01*. 2026.

The archived specification DOI can be added after release. It will identify this specification, separately from any DOI assigned to a PAD dataset release.

## Structural checks

With `jsonschema` 4.x installed, run `python -m unittest discover -s tests -v` from the repository root. The tests validate the illustrative JSON schema and fictional fixture, check its internal references and reject selected malformed records. See `docs/VALIDATION_REPORT.json` for the scope of verification.
