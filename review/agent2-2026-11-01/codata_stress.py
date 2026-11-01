import sys,json; sys.path.insert(0,'../candidate/PAR_Core_Mature_Candidate_2026-11-01/tools')
from validate_par import validate
# Shape of a metrology "recommended value" record. Numbers NOT source-validated (memory only); structure is under test.
rec={
 "schema_version":"0.2.0-candidate","par_id":"urn:uuid:agent2-stress-0001","par_version":"1","record_status":"draft",
 "record_identity":{"revision_kind":"initial","predecessors":[]},
 "proposition":{"type":"quantitative","quantity":{"scheme":"QUDT","value":"GravitationalConstant"},
   "result":{"state":"observed","value":6.67430e-11,"unit":{"scheme":"ucum","value":"m3.kg-1.s-2"},
             "uncertainty":{"kind":"standard_deviation","value":1.5e-15}},   # GUM 'standard uncertainty' has no enum slot
   "estimand":"least-squares adjusted recommended value over selected experiments","parameter":{"scheme":"local","value":"G"}},
 "interpretation":{"polarity":"affirmative","epistemic_status":"asserted","conflict_status":"reported_conflict"},
 "scope":{"observed_system":{"scheme":"local","value":"ensemble-of-torsion-balance-and-other-experiments"},
          "claimed_system":{"scheme":"local","value":"universal"},"unit_of_observation":"one adjusted ensemble",
          "aggregation_level":"other","projection":{"kind":"inference","basis":"least-squares adjustment with expanded uncertainties to account for inter-experiment inconsistency"},
          "context":[]},
 "evidence":[],
 "provenance":{"original_issuer":{"scheme":"ROR","value":"task-group"},
   "origin":{"kind":"analysis_artifact","identifier":{"scheme":"DOI","value":"10.xxxx/placeholder"},"locator":"Table of recommended values"},
   "activities":[],"distribution":[]},
 "derivation":{"kind":"analysis","components":[]},   # inputs are ~15 experiments that are NOT PARs: no slot for non-PAR components
 "verification":{"status":"unverified","reviewers":[]},
 "rights":{"access":"open","statement":"placeholder","source":{"kind":"publication","identifier":{"scheme":"DOI","value":"10.xxxx/placeholder"},"locator":"front matter"}},
 "profiles":[]}
print("core gate:", validate(rec) or "PASS")
rec["uncertainty_kind_attempt"]="standard_uncertainty"
print("with GUM term as extra field:", validate(rec)[:1])
