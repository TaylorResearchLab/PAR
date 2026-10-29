"""Structural checks for the fictional v0.01 JSON fixture.

Run: python -m unittest discover -s tests -v
Requires jsonschema 4.x. These tests are not source-fidelity validation.
"""
import copy
import json
from pathlib import Path
import unittest
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]

class DraftProfileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads((ROOT / 'schemas/par-core-0.01.schema.json').read_text())
        cls.example = json.loads((ROOT / 'examples/synthetic_single_assertion.json').read_text())
        cls.validator = Draft202012Validator(cls.schema, format_checker=FormatChecker())

    def test_schema_is_valid(self):
        Draft202012Validator.check_schema(self.schema)

    def test_example_is_structurally_valid(self):
        self.validator.validate(self.example)
        self.assertTrue(self.example['example_fixture'])

    def test_claim_references(self):
        claim = self.example['claim']
        ids = {n['id'] for n in claim['graph']['nodes']}
        predicates = {p['iri'] for p in self.example['semantics']['predicates']}
        rels = claim['graph']['relationships']
        self.assertEqual(set(claim['boundary']['relationship_ids']), {r['id'] for r in rels})
        for rel in rels:
            self.assertIn(rel['subject'], ids)
            self.assertIn(rel['object'], ids)
            self.assertIn(rel['predicate'], predicates)
        for point in claim['connection_points']:
            self.assertTrue(any(n['id'] == point and n.get('iri') for n in claim['graph']['nodes']))

    def test_missing_core_fields_rejected(self):
        for field in ['id', 'origin', 'claim', 'semantics', 'evidence']:
            with self.subTest(field=field):
                record = copy.deepcopy(self.example)
                del record[field]
                self.assertTrue(list(self.validator.iter_errors(record)))

    def test_empty_connection_points_rejected(self):
        record = copy.deepcopy(self.example)
        record['claim']['connection_points'] = []
        self.assertTrue(list(self.validator.iter_errors(record)))

    def test_undefined_predicate_iri_rejected(self):
        record = copy.deepcopy(self.example)
        record['claim']['graph']['relationships'][0]['predicate'] = 'undefined'
        self.assertTrue(list(self.validator.iter_errors(record)))

if __name__ == '__main__':
    unittest.main()
