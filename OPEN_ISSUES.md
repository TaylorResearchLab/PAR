# Decisions for v0.01 review

1. **Authorship and stewardship.** Confirm the specification author list, maintainer and approving authority before an archival release. The current editor attribution is Deanne M. Taylor.
2. **Licensing checks for new material.** The specification and documentation use CC BY 4.0; schemas, code and JSON fixtures use MIT. Check new contributions and any third-party material against the scope in `LICENSE.md`.
3. **Repository and archive.** The public repository is TaylorResearchLab/PAR. Confirm the approved archival release and Zenodo metadata separately from publication of working drafts.
4. **Publication and source locators.** Confirm the Core requirement of a publication or DOI-identified data source. Decide how to admit valuable legacy source records lacking either while retaining an explicit conformance distinction.
5. **Identifier and version policy.** Select the persistent identifier registry or minting convention, retention policy and treatment of retrospective source corrections. Content hashes alone do not define scientific identity.
6. **Compound-claim tests.** Establish examples and review criteria for minimal inseparability. A graph being connected is necessary for the selected compound-claim representation but insufficient to prove that it expresses one claim.
7. **First claim profiles.** Define separate context and evidence requirements for observations, curated associations, assessments and computational inferences. Determine the initial biomedical subset.
8. **JKG and RDF adapters.** Pin the JKG version and map actual structures. Develop and test an RDF serialization and SHACL constraints rather than assuming the illustrative JSON envelope supplies either.
9. **Reconciliation procedure.** Specify how verified same-origin records receive a canonical PAR identifier across independent producers, including merge and split history.
10. **Genealogy granularity.** Establish controlled relations for shared publications, observations, cohorts and experiments. Clarify what documented checks warrant an independence claim.
11. **Review and release.** Define review-status vocabulary and who may approve scientific acceptance and distribution in each implementation. Record structural, semantic and source-fidelity results separately.
12. **Round-trip tests.** Establish fixtures that preserve claim meaning through JSON, RDF, tabular and property-graph transformations. This draft includes only a structural JSON example.
