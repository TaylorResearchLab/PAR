#!/usr/bin/env python3
"""Agent 2 (PAR-Claude-20261101-01) negative controls against PAR Core 0.2.0-candidate.

Each control is a record that SHOULD be rejected (or a property that SHOULD hold) under the
accepted scientific decisions, run through the candidate's own validate() unchanged.
Outcome 'FALSE_PASS' = validator accepted a record that violates an accepted invariant.
Outcome 'REJECTED'   = validator correctly rejected it.
Outcome 'OBSERVED'   = structural property measured (not pass/fail).
"""
import copy, json, math, sys
from pathlib import Path

CAND = Path(sys.argv[1])
sys.path.insert(0, str(CAND / "tools"))
from validate_par import validate, CORE  # noqa: E402  (frozen candidate code, unchanged)

def fx(name):
    return json.loads((CAND / "fixtures" / f"{name}.json").read_text())

results = []
def control(cid, title, record, release=False, expect_reject=True, note=""):
    errs = validate(record, release)
    accepted = not errs
    if expect_reject:
        outcome = "FALSE_PASS" if accepted else "REJECTED"
    else:
        outcome = "ACCEPTED" if accepted else "UNEXPECTED_REJECT"
    results.append({"id": cid, "title": title, "gate": "release" if release else "core",
                    "outcome": outcome, "errors": errs[:3], "note": note})

# ---------------------------------------------------------------- identity / revision
r = fx("physical_measurement")
r["record_identity"]["revision_kind"] = "scientific_revision"
r["record_identity"]["predecessors"] = [{"par_id": "urn:uuid:completely-unrelated", "par_version": "9"}]
control("NC-01", "scientific_revision whose predecessor is a different par_id (lineage to a foreign record)", r, True,
        note="No check that predecessor shares par_id or origin_assertion_identifier; identity continuity unenforced.")

r = fx("physical_measurement")
r["record_identity"]["revision_kind"] = "representation_correction"
r["record_identity"]["predecessors"] = [{"par_id": r["par_id"], "par_version": "1"}]
r["par_version"] = "0"
control("NC-02", "version '0' claims predecessor version '1' of same par_id (lineage runs backward)", r, True,
        note="par_version is an unordered string; no monotonicity or acyclicity check.")

r = fx("physical_measurement")
r["record_identity"]["revision_kind"] = "representation_correction"
r["record_identity"]["predecessors"] = [{"par_id": r["par_id"], "par_version": "0"}]
r["par_version"] = "1"
r["proposition"]["result"]["value"] = 9.99  # value changed under a 'representation_correction'
control("NC-03", "representation_correction changes the measured value (meaning change disguised as representation fix)", r, True,
        note="Validator cannot see predecessor content; revision_kind is a self-declaration with no diff check.")

# ---------------------------------------------------------------- composition / inheritance
r = fx("composed_with_own_evidence")
r["evidence"] = [copy.deepcopy(fx("physical_measurement")["evidence"][0])]   # verbatim copy of the input's evidence
control("NC-04", "composition whose only evidence is a verbatim copy of its input's instrument evidence, inherited_evidence=false", r, True,
        note="Evidence inheritance by copy is undetectable; the const-false flag is vacuous.")

r = fx("composed_with_own_evidence")
r["derivation"]["activity_id"] = "analysis-7"
r["provenance"]["activities"] = []   # already empty in fixture; activity_id resolves to nothing
control("NC-05", "composition cites activity_id 'analysis-7' that appears in no provenance.activities entry", r, True,
        note="Dangling activity reference accepted; the derivation is untraceable despite 'traceable evidence'.")

r = fx("composed_with_own_evidence")
r["proposition"]["result"]["state"] = "observed"
r["evidence"][0]["basis"] = "computational_inference"
control("NC-06", "composition declares result.state=observed with only computational_inference evidence and an instrument origin copied from the input", r, True,
        note="observed vs inferred is not cross-checked against evidence.basis or derivation.kind.")

# ---------------------------------------------------------------- evidence semantics
r = fx("not_derivable_draft")
control("NC-07", "not_derivable outcome attached to basis=experimental_measurement, source.kind=instrument_record (fixture as shipped)", r, False, expect_reject=True,
        note="A failed derivation is attributed to an instrument trace, not to an analysis artifact; outcome/basis/source.kind not cross-checked.")

r = fx("physical_measurement")
r["evidence"][0].update({"direction": "supports", "outcome": "failed"})
control("NC-08", "evidence direction=supports with outcome=failed", r, True,
        note="A failed procedure cannot support a measured value; no direction/outcome coherence rule.")

r = fx("null_result")
control("NC-09", "null_result fixture as shipped: epistemic_status=observed, polarity=affirmative, result.state=not_observed", r, True,
        note="Record asserts an affirmative observed claim about a quantity that was not observed.")

r = fx("physical_measurement")
r["evidence"].append(copy.deepcopy(r["evidence"][0]))
r["evidence"][1]["evidence_id"] = "ev-physical-002"
r["evidence"][1]["independence"] = "assessed_independent"
control("NC-10", "two evidence items, identical source identifier+locator, second self-declared assessed_independent", r, True,
        note="Independence is a free self-declaration; identical locators not detected even within one record.")

r = fx("physical_measurement")
r["evidence"][0]["source"]["locator"] = "x"
r["evidence"][0]["source"]["identifier"] = {"scheme": "?", "value": "?"}
control("NC-11", "released record whose sole evidence locator is 'x' and identifier scheme/value are '?'", r, True,
        note="Traceability threshold is minLength=1; any non-empty string is a 'precise locator'.")

r = fx("physical_measurement")
r["evidence"][0]["source"]["retrieved_at"] = "yesterday, probably"
control("NC-12", "retrieved_at='yesterday, probably' with format:date-time", r, True,
        note="FormatChecker without rfc3339-validator silently skips date-time; passes in the shipped environment spec.")

r = fx("physical_measurement")
r["verification"]["status"] = "failed"
control("NC-13", "record_status=released with verification.status=failed", r, True,
        note="Release gate ignores a recorded failed source check.")

r = fx("physical_measurement")
r["record_status"] = "withdrawn"
r["record_identity"]["successors"] = []
control("NC-14", "withdrawn record with no successors and no reason slot", r, False, expect_reject=False,
        note="OBSERVED: withdrawal carries no reason/field; a retracted claim is indistinguishable from a superseded one.")

# ---------------------------------------------------------------- quantitative
r = fx("physical_measurement")
r["proposition"]["result"]["value"] = float("nan")
control("NC-15", "observed value NaN (Python json accepts; JSON does not)", r, True,
        note="jsonschema 'number' admits NaN; interval checks with NaN compare False.")

r = fx("physical_measurement")
r["proposition"]["result"]["uncertainty"] = {"kind": "confidence_interval", "lower": float("nan"), "upper": 1, "level": 0.95}
control("NC-16", "CI with lower=NaN", r, True, note="lower>upper is False for NaN; semantic check bypassed.")

r = fx("physical_measurement")
r["proposition"]["result"]["uncertainty"] = {"kind": "confidence_interval", "lower": 10, "upper": 20, "level": 0.95}
# value 4.12 lies outside [10,20]
control("NC-17", "point value 4.12 outside its own 95% CI [10,20]", r, True,
        note="No value-within-interval check.")

r = fx("physical_measurement")
r["proposition"]["result"]["uncertainty"] = {"kind": "exact", "upper": 5, "level": 0.5, "parameters": {"sigma": 2}}
control("NC-18", "uncertainty kind=exact carrying upper, level and parameters", r, True,
        note="The not-anyOf guard forbids value/lower/distribution only; upper/level/parameters leak through.")

r = fx("physical_measurement")
r["proposition"]["result"]["uncertainty"] = {"kind": "standard_error", "value": 0}
control("NC-19", "standard_error = 0 on a physical measurement (exact disguised as SE)", r, True,
        note="Non-negativity check admits zero spread; no distinction from kind=exact.")

r = fx("physical_measurement")
r["proposition"]["result"]["unit"] = {"scheme": "unit", "value": "furlongs per fortnight per kelvin"}
r["proposition"]["quantity"] = {"scheme": "local", "value": "decay-rate"}
control("NC-20", "decay-rate reported in 'furlongs per fortnight per kelvin'", r, True,
        note="Unit is an opaque identifier; dimensional consistency with quantity is not representable, so not checkable.")

r = fx("physical_measurement")
r["proposition"]["result"] = {"state": "censored", "censoring": "below detection limit", "unit": {"scheme": "unit", "value": "s^-1"}}
control("NC-21", "censored result with detection limit only in prose, no numeric bound slot", r, False, expect_reject=False,
        note="OBSERVED: schema has no numeric censoring bound; limit of detection is unrecoverable by machine.")

r = fx("physical_measurement")
r["interpretation"]["polarity"] = "negative"
control("NC-22", "quantitative proposition with polarity=negative ('decay-rate is NOT 4.12 +/- 0.15'?)", r, False, expect_reject=False,
        note="OBSERVED: negation of a measurement has undefined semantics but is accepted.")

# ---------------------------------------------------------------- scope / aggregation
r = fx("physical_measurement")
r["scope"]["aggregation_level"] = "population"
r["scope"]["unit_of_observation"] = "one instrument run"
control("NC-23", "aggregation_level=population from unit_of_observation='one instrument run' (ecological inflation)", r, True,
        note="Single aggregation_level field; no observed-vs-claimed aggregation, so the ecological guard cannot be expressed.")

r = fx("scope_projection_draft")
r["scope"]["projection"]["basis"] = "because"
control("NC-24", "projection basis = 'because'", r, False, note="Basis presence only (acknowledged in KNOWN_GAPS 9). Gate corrected to core on 2026-11-01 after LOG-009; fixture is a draft, so the release gate rejected it for empty evidence, not for the basis.")

r = fx("physical_measurement")
r["scope"]["projection"] = {"kind": "transport", "basis": "n/a"}
control("NC-25", "projection kind=transport while observed_system == claimed_system", r, True,
        note="Projection declared where none occurred; no contradiction flagged.")

# ---------------------------------------------------------------- process / conjecture
r = fx("process")
r["proposition"]["transitions"] = []
r["proposition"]["steps"] = r["proposition"]["steps"][:1]
control("NC-26", "process with one step and zero transitions", r, True,
        note="A 'process' with no ordering or transition is accepted; transitions minItems=0.")

r = fx("process")
r["proposition"]["transitions"] = [{"from": "step-a", "to": "step-a", "relation": "precedes"}]
control("NC-27", "process transition step-a precedes step-a (self-loop) and step-b unreachable", r, True,
        note="No acyclicity/reachability; endpoints exist so check passes.")

r = fx("conjecture_draft")
r["record_status"] = "released"
r["evidence"] = [copy.deepcopy(fx("physical_measurement")["evidence"][0])]
r["interpretation"]["epistemic_status"] = "observed"
control("NC-28", "proposition.type=conjecture, epistemic_status=observed, released with supporting positive evidence", r, True,
        note="Type-level 'conjecture' and status-level 'observed' coexist; the two encodings of epistemic stance are unreconciled.")

r = fx("conjecture_draft")
control("NC-29", "conjecture_draft as shipped: provenance.origin is instrument-run-17 (a hypothesis 'originating' from an instrument trace)", r, False, expect_reject=True,
        note="origin.kind enum has no slot for an asserted/authored proposition; provenance forces a source_locator on an idea.")

# ---------------------------------------------------------------- profile extensibility
r = fx("physical_measurement")
r["profiles"] = [{"identifier": {"scheme": "par-profile", "value": "devmap-chd"}, "version": "0.1"}]
r["profile_data"] = {"hpo_term": "HP:0001631"}
control("NC-30", "record declaring a profile and carrying one profile-specific field at root", r, False, expect_reject=False,
        note="EXPECT REJECT by additionalProperties=false: profiles cannot add any field anywhere; extensibility claim is unimplementable.")

r = fx("physical_measurement")
r["proposition"]["profile_ext"] = {"x": 1}
control("NC-31", "profile field inside proposition", r, False, expect_reject=False, note="Same: additionalProperties=false on every object.")

# ---------------------------------------------------------------- cross-record (PAD-level) observations
fixtures = [p.stem for p in (CAND / "fixtures").glob("*.json")]
recs = {n: fx(n) for n in fixtures}
oai = {}
for n, rec in recs.items():
    k = json.dumps(rec["record_identity"].get("origin_assertion_identifier"), sort_keys=True)
    oai.setdefault(k, []).append(n)
shared = {k: v for k, v in oai.items() if len(v) > 1}
results.append({"id": "OBS-01", "title": "fixtures sharing one origin_assertion_identifier", "gate": "corpus", "outcome": "OBSERVED",
                "errors": [], "note": json.dumps(shared)})
evid = {}
for n, rec in recs.items():
    for e in rec["evidence"]:
        evid.setdefault((e["evidence_id"], e["source"]["locator"]), []).append((n, e["direction"], e["outcome"]))
results.append({"id": "OBS-02", "title": "same evidence_id+locator used across fixtures with differing direction/outcome", "gate": "corpus", "outcome": "OBSERVED",
                "errors": [], "note": json.dumps({f"{k[0]}@{k[1]}": v for k, v in evid.items() if len(v) > 1})})

# ---------------------------------------------------------------- test-suite audit
results.append({"id": "OBS-03", "title": "tests that do not exercise the validator", "gate": "tests", "outcome": "OBSERVED", "errors": [],
                "note": "test_22 and test_38 assert fixture-file contents only; test_40 (json.loads(json.dumps(r))==r) is true for any JSON; "
                        "test_39 asserts rights=unknown passes release gate, codifying the acknowledged gap as expected behaviour; "
                        "test_14 asserts validity only, not that two distributions resolve to one origin."})

for x in results:
    print(json.dumps(x))
counts = {}
for x in results:
    counts[x["outcome"]] = counts.get(x["outcome"], 0) + 1
print(json.dumps({"summary": counts}))
