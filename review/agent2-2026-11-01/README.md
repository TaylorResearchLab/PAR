# Agent 2 independent review of PAR Core 0.2.0-candidate

Reviewer instance: `PAR-Claude-20261101-01` (SCUTER Agent 2). Date: 2026-11-01.
Governing record: PAR Collaboration Log LOG-008
(https://app.notion.com/p/40b29187800881238e90eeaa8534d82e); registration LOG-007
(https://app.notion.com/p/40b29187800881d4a921f943a11e3ad6).

This branch is review material. It is not a specification change, not accepted state,
and must not be merged into `main`. `main` at `d658a7117489faa746dc91fcacf15c4e6dea82ee`
remains the provisional v0.01 scaffold.

## Contents

- `candidate/PAR_Core_Mature_Candidate_0.2.0_2026-11-01.zip`: the exact frozen artifact
  reviewed, authored by Agent 1 `PAR-GPT-20261031-02`. SHA-256
  `444169807e31caacb8d7e2422585729864fd6fcb17c377cb81d945e962615820` (matches LOG-005/006).
  Included for durable custody; previously existed only as chat attachments.
- `candidate/PAR_Claude_Agent2_Handoff_2026-11-01.md`: Agent 1 handoff, SHA-256
  `fefc168c123f8da4bfa81d69fcd419af7065bd1d3f9d1cb4f1a7768609096919`.
- `negative_controls.py`: 31 controls run through the candidate's own `validate()` unchanged.
- `negative_controls_output.jsonl`: recorded outcomes (25 FALSE_PASS, 3 ACCEPTED, 1 REJECTED,
  2 UNEXPECTED_REJECT, 3 OBSERVED).
- `codata_stress.py`: non-biomedical metrology-shaped record; numeric values are not
  source-validated, structure is the test object.
- `environment.txt`, `SHA256SUMS.txt`.

## Reproduce

```sh
unzip candidate/PAR_Core_Mature_Candidate_0.2.0_2026-11-01.zip -d /tmp/cand
cd /tmp/cand/PAR_Core_Mature_Candidate_2026-11-01
sha256sum -c reports/manifest_sha256.txt          # 25 OK
python3 -I -m unittest discover -s tests -v       # 40 OK
cd -
python3 -I negative_controls.py /tmp/cand/PAR_Core_Mature_Candidate_2026-11-01
python3 -I codata_stress.py                       # expects ../candidate/... layout; adjust sys.path if needed
```

Environment used: Python 3.13.18, jsonschema 4.26.0, `rfc3339-validator` absent.

Structural results only. No source fidelity, prior art, or scientific acceptance is established here.
