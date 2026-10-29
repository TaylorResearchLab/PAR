# Portable Assertion Records (PAR)
## Proposed specification v0.01

**Editor:** Deanne M. Taylor  
**Draft date:** 29 October 2026  
**Status:** Initial proposal for review. Field names and serialization profiles may change before an approved release.

## 1. Purpose

A Portable Assertion Record (PAR) carries a scientific claim together with the information needed to interpret, trace and reuse it. The claim may be an observation, an expert assessment, a curated relationship or a computational inference. Its scientific meaning, source context and provenance travel with the record when it is extracted from a database, exchanged between systems or assembled into a new knowledge graph.

PAR defines a reuse contract across data models. It specifies what a record must preserve rather than requiring a particular graph database or storage format. A conforming RDF graph or dataset can be a PAR. JSON, relational tables and property-graph exports can represent the same record through documented serialization profiles. Each transformation must preserve the declared claim and identify any changes in its representation.

The initial application is extraction and provenance enrichment of the Data Distillery Knowledge Graph (DDKG). The Core contract is intended for scientific claims across disciplines. Biomedical profiles will supply domain-specific context without making those fields universal requirements.

## 2. Terms and conformance

In this draft, **MUST** identifies a Core requirement, **SHOULD** identifies a recommended practice and **MAY** identifies an option. These words describe the proposed contract in this document; v0.01 is not an adopted community standard.

An **assertion** is a claim attributed to an originating issuer. **Evidence** consists of observations, experiments, analyses or other material offered in support of, or against, a claim. **Provenance** records where the assertion came from and how the record was constructed or changed. **Authority** identifies the responsible source and its role. **Context** describes the conditions and scope in which the claim is stated. These roles must remain distinguishable even when one publication supplies more than one of them.

A **PAR identifier** identifies an assertion record. A **record version** identifies a particular state of that record. A **profile** adds requirements for a class of scientific claims. A **Portable Assertion Database (PAD)** is a collection of PARs with a release manifest and associated resources.

Conformance has three separately reported dimensions:

1. **Structural conformance:** required fields, identifier syntax and references satisfy the declared serialization profile.
2. **Semantic conformance:** the record identifies a coherent claim boundary and preserves source meaning, direction and required context.
3. **Source fidelity:** the assertion and its attribution can be checked against the identified origin.

A validator may establish structural conformance. Semantic and source-fidelity checks require source-aware procedures and recorded review. A conformance result describes the record's representation; confidence in the scientific claim depends on its evidence and intended use.

## 3. Claim boundary and graph structure

A PAR MUST contain either one scientific assertion or a minimally inseparable connected set of component assertions that jointly express an overarching claim. It MUST identify the included claim components. For a compound claim, it MUST state why the components belong together and how they express that claim. A pathway statement, for example, may require an ordered series of events and their joint conditions.

Relationships that can be interpreted and attributed independently SHOULD be represented as separate PARs. They can be joined through shared identifiers. The number of graph edges alone does not determine the number of assertions: a qualified relationship may require several structural edges to express one scientific statement.

The record MUST distinguish claim content from the metadata that describes its source, curation or distribution. It MUST declare at least one connection point carrying a defined Internationalized Resource Identifier (IRI). This is the minimum anchor for joining the record to another graph. Other nodes may have record-local identifiers, provided their scope and references are explicit.

Each relationship MUST have a defined predicate IRI and an explicit subject-to-object orientation. Predicate definitions MUST describe the intended meaning and expected endpoint roles. A symmetric predicate still has ordered endpoints in its serialization; the predicate definition declares symmetry.

Connection-point and predicate identifiers MAY belong to a community namespace or a declared internal namespace. Compact identifiers MUST include an unambiguous expansion to an IRI. Definitions MUST accompany the record or be available through an identified, versioned reference. HTTP resolution is useful but not required for every IRI. Shared identifiers provide join points; equality of labels alone does not establish identity.

## 4. PAR Core

A Core record MUST contain the following information. The names in parentheses illustrate the JSON profile and are not universal wire-format requirements.

### 4.1 Record identity and version

The record MUST have a persistent globally unique identifier (`id`), an immutable record-version identifier (`version`) and the specification version it follows (`spec_version`). A UUID-based URN is one suitable identifier form. A registry may supply another globally unique IRI scheme. An individual PAR does not require a DOI.

A changed published record MUST receive a new version. Earlier versions MUST remain identifiable. The record SHOULD identify its predecessor and describe substantive changes. A correction to the representation of the same originating claim may retain the PAR identifier with a new version. A new originating claim or a distinct assessment receives its own PAR identifier and a typed relationship to related records.

### 4.2 Source-qualified claim

The claim MUST have a declared class and boundary. Its source-native statement MUST be retained as a permitted text excerpt, structured assertion or precise locator that supports reconstruction of the statement. Profiles MUST describe how the source-native representation maps to the portable representation.

The claim graph MUST declare its entities, relationships and connection points. Every endpoint reference MUST resolve within the record or through an explicitly declared external reference. Source-native identifiers and harmonized identifiers MUST remain distinguishable. Mappings MUST record their asserted relation, such as exact identity, broader meaning or an unresolved candidate mapping, with attribution. Mapping to a shared integrated Concept does not by itself establish equivalence of every attached source identifier.

### 4.3 Traceable origin and attribution

Every PAR MUST identify a traceable originating claim in a publication or a DOI-identified data source. A publication may be identified by a DOI, PMID or other persistent locator with sufficient bibliographic information to identify it. For a data source, its DOI identifies the source release or dataset; the assertion's native record identifier and locator MUST also be supplied when applicable. An exact source version, release or retrieval snapshot MUST be recorded when available. When the source exposes no version, the record MUST state that fact and retain the retrieval date and locator.

The origin MUST identify the issuer responsible for the claim. Redistribution and extraction resources MUST be recorded separately. A database that republishes an assertion is part of its distribution lineage; it is not automatically the originating issuer. A database's own independently curated assessment may itself be an originating assertion.

Each construction or transformation activity MUST identify the responsible actor or software, its role and the inputs it used. The record MUST retain source releases and extraction or ingestion versions used to reconstruct the assertion. Known curation criteria, review outcomes and responsible organizations SHOULD accompany the record. An unavailable actor name is represented as unknown, rather than assigned to an unrelated redistributor.

### 4.4 Context and qualifications

Each selected profile MUST identify which contextual fields are necessary to interpret its claim class. Their values MUST carry a status: `source_stated`, `inherited`, `curated`, `inferred`, `unknown` or `not_applicable`. Inherited, curated and inferred values MUST identify the source or activity that supplied them. These categories describe how the context was obtained, not the strength of the evidence.

A profile for an inheritance-specific gene–disease assertion requires inheritance mode. A quantitative observation requires units and the relevant measurement conditions. A general association profile may have different requirements. Missing context is explicitly recorded. A missing value is distinct from an observed absence or a negative result.

### 4.5 Evidence and genealogy

The record MUST declare its evidence-availability state and retain evidence references supplied by the source. Evidence items SHOULD identify the originating observation or experiment as precisely as access and source detail permit. A record MAY cite several publications supporting one originating assertion.

Evidence links MUST distinguish support, contradiction, qualification and contextual relevance when those roles are established. Source-reported assessments and confidence qualifications MUST retain their issuer, meaning and applicable scale. They MUST remain distinguishable from newly computed scores.

Shared evidence MUST be represented through explicit links where established. Genealogy states MUST distinguish `confirmed_shared`, `probable_overlap`, `unresolved` and any claim of independence supported by a documented procedure. A shared DOI indicates a common publication; it does not establish that two records describe the same observation. Different DOIs likewise do not establish independent evidence.

### 4.6 Rights, integrity and review

The record MUST state the rights and access conditions applicable to its content and identify the source of that information. A record that combines materials with different conditions MUST retain those distinctions. Core conformance does not grant redistribution rights.

A record MUST expose its review status and the associated decision history. A released representation SHOULD carry a checksum or be covered by a checksummed PAD manifest. Checksums identify particular bytes and their serialization. Hashes from different valid serializations are not interchangeable unless a declared canonicalization procedure establishes that relation.

## 5. Reconciliation and assertion identity

Repeated representations of the **same originating claim** are reconciled into one PAR with cross-references to the resources that carry it. Reconciliation MUST consider the source record, claim content and context. A shared publication, identical subject–predicate–object triple or matching text alone is insufficient.

Distinct originating assertions remain distinct PARs even when their content agrees. Distinct expert assessments remain distinct when their issuers, criteria or assessment events differ. They may reference the same evidence. A synthesized claim produced by combining existing PARs is a derived assertion with its own identity, construction activity and links to the input PAR identifiers and versions. To qualify as a source-grounded PAR, that derived assertion must identify its own originating publication or DOI-identified data source under §4.3. Until then it remains a derived candidate. Input-PAR citations document its inputs rather than assigning the new claim to an earlier issuer.

Where identity is unresolved, the record collection MUST retain the competing candidates and the reason for ambiguity. A producer MUST not merge candidates merely to reduce record counts. Consumers can group agreeing claims for presentation while preserving their underlying identities.

## 6. Extraction and recovery

DDKG extraction is one source-adapter implementation of the general contract. It uses Concept membership, source Codes, SAB attribution and ingestion records to locate source-native assertions. Recovery is recorded as one of four alternatives:

- `exact`: the originating source record is directly identifiable.
- `join_recoverable`: matching identifiers across source tables identifies the originating record.
- `ambiguous`: multiple candidate originating records remain.
- `unavailable`: the required source information cannot be obtained.

Each decision MUST carry its rationale and the input graph and ingestion versions. Recovery status describes source reconstruction, not scientific confidence. An extracted candidate with an unresolved originating claim can remain in a recovery inventory. It is promoted to a source-grounded PAR when the Core origin requirements are met. A PAD may distribute a separately labeled candidate inventory with permitted content; candidates and conforming PARs require separate manifest counts.

## 7. Serialization and schema profiles

### JSON and JKG

A JSON serialization profile defines the envelope, graph representation and names of fields that implement the Core. JSON Schema can test declared structural requirements. The initial reference direction is compatibility with JSON Knowledge Graph (JKG) graph-bearing structures. A production JKG adapter must identify the exact JKG specification version and demonstrate preservation of claim boundaries, identifiers and provenance.

The included `par-core-0.01.schema.json` is an **illustrative draft JSON envelope**, not a completed JKG implementation. Its accompanying example establishes structural behavior only. Cross-reference resolution, graph connectedness, source fidelity and rights checks remain additional validation stages.

### RDF

An RDF graph or dataset qualifies as a PAR when it meets the same Core contract and identifies which statements are assertion content and which describe provenance, context or publication information. A profile may use named graphs and established vocabularies such as PROV-O. SHACL can express structural constraints. RDF blank nodes are scoped to their containing representation and must not be treated as globally shared join identifiers.

### Other representations

Tabular and property-graph representations MUST provide a mapping to Core concepts and retain record identity through reconstruction. A target schema that cannot express a qualification may preserve it in an associated record. Any transformation that changes or omits claim meaning MUST expose that change and its relation to the source PAR.

## 8. PAD releases and computational access

A PAD release MUST identify its release version and list the PAR identifier and record version for each member. Its manifest MUST identify the specification and profiles used, source releases, content hashes, access conditions and the status of included records. Candidate inventories and source-recovery exclusions MUST be identified separately from conforming PARs.

An archived PAD may receive a version-specific DOI. That DOI cites the collection release; individual PAR identifiers cite constituent assertions. A specification release may separately receive its own DOI. These identifiers have different scopes.

File, SQL, graph and tool interfaces SHOULD return record identifiers and versions with their results. An AI-facing tool SHOULD retain the query, PAD release and transformations needed to reconstruct the returned assertion set. Retrieval limits and unavailable or restricted records SHOULD be explicit in the response. An MCP service is one access implementation, not a requirement for PAR conformance.

## 9. Worked examples

`examples/synthetic_single_assertion.json` demonstrates one assertion with two identified entities, a defined predicate and one connection point. Its publication and entities use `example.org` identifiers and are fictional test fixtures, not scientific evidence.

`examples/README.md` explains how the same structure extends to compound claims, distinct assessments and redistributed records. Actual AFF4–CHOPS DDKG relationships motivate the framework, but their originating evidence must be recovered before constructing source-grounded examples that imply such provenance.

## 10. Versioning and development

Version v0.01 records the initial proposed contract. Subsequent drafts should publish changes to requirement meaning, record fields, profiles and migration guidance. A release SHOULD include its specification, schemas, examples, validation results, citation metadata and change log. Decisions listed in `OPEN_ISSUES.md` remain explicit rather than silently becoming requirements.

## References

- Cyganiak R, Wood D, Lanthaler M, editors. *RDF 1.1 Concepts and Abstract Syntax*. W3C Recommendation, 2014. https://www.w3.org/TR/rdf11-concepts/
- Lebo T, Sahoo S, McGuinness D, editors. *PROV-O: The PROV Ontology*. W3C Recommendation, 2013. https://www.w3.org/TR/prov-o/
- Knublauch H, Kontokostas D, editors. *Shapes Constraint Language (SHACL)*. W3C Recommendation, 2017. https://www.w3.org/TR/shacl/
- Wright A, Andrews H, Hutton B, Dennis G. *JSON Schema: A Media Type for Describing JSON Documents*. Draft 2020-12, 2022 publication. https://json-schema.org/draft/2020-12/json-schema-core

