#!/usr/bin/env python3
"""Executable teaching fixture: review receipts, durable budget, effect recovery.

Run from the guide root: python3 examples/workflows/review-control-demo.py
Stdlib only. All effects occur in disposable SQLite databases. No GitHub calls.
The caller supplies trusted expected fields; matching a producer label is NOT
authentication. The fake destination supports idempotency; real services need
their own integration tests. This is not a production merge controller.
"""
import concurrent.futures
from contextlib import closing
import hashlib
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path


def unique_fields(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate receipt field')
        result[key] = value
    return result


def verdict(raw, expected, now):
    """Fail closed on malformed, stale, partial, foreign or refusing evidence."""
    try:
        receipt = json.loads(raw, object_pairs_hook=unique_fields)
        if not isinstance(receipt, dict) or set(receipt) != {
            'producer', 'version', 'run', 'revision', 'scope', 'status',
            'decision', 'expires', 'complete',
        }:
            return 'UNKNOWN'
        if any(receipt.get(key) != value for key, value in expected.items()):
            return 'UNKNOWN'
        if type(receipt['expires']) is not int or receipt['expires'] <= now:
            return 'UNKNOWN'
        if receipt['complete'] is not True or receipt['status'] != 'SUCCEEDED':
            return 'UNKNOWN'
        if receipt['decision'] == 'REJECT':
            return 'REJECT'
        return 'ACCEPT' if receipt['decision'] == 'ACCEPT' else 'UNKNOWN'
    except (TypeError, ValueError, KeyError):
        return 'UNKNOWN'


def connect(path):
    return closing(sqlite3.connect(path, timeout=10, isolation_level=None))


class Destination:
    """Fake external service with a UNIQUE idempotency key and observable state."""
    def __init__(self, path):
        self.path = path
        self.available = True
        with connect(path) as db:
            db.execute('CREATE TABLE IF NOT EXISTS effects (id TEXT PRIMARY KEY, digest TEXT)')

    def apply(self, effect_id, digest):
        if not self.available:
            raise ConnectionError('Destination state unavailable')
        with connect(self.path) as db:
            db.execute('BEGIN IMMEDIATE')
            old = db.execute('SELECT digest FROM effects WHERE id=?', (effect_id,)).fetchone()
            if old and old[0] != digest:
                db.rollback()
                raise ValueError('Idempotency key reused for different content')
            db.execute('INSERT OR IGNORE INTO effects VALUES (?,?)', (effect_id, digest))
            db.commit()

    def lookup(self, effect_id):
        if not self.available:
            raise ConnectionError('Destination state unavailable')
        with connect(self.path) as db:
            row = db.execute('SELECT digest FROM effects WHERE id=?', (effect_id,)).fetchone()
            return row[0] if row else None

    def count(self):
        with connect(self.path) as db:
            return db.execute('SELECT count(*) FROM effects').fetchone()[0]


class Controller:
    def __init__(self, path, budget):
        self.path = path
        with connect(path) as db:
            db.execute('CREATE TABLE IF NOT EXISTS budget (id INTEGER PRIMARY KEY, remaining INTEGER)')
            db.execute('INSERT OR IGNORE INTO budget VALUES (1,?)', (budget,))
            db.execute('CREATE TABLE IF NOT EXISTS journal (id TEXT PRIMARY KEY, digest TEXT, state TEXT)')

    def remaining(self):
        with connect(self.path) as db:
            return db.execute('SELECT remaining FROM budget WHERE id=1').fetchone()[0]

    def perform(self, raw, expected, now, effect_id, destination, crash=None,
                check=verdict):
        try:
            decision = check(raw, expected, now)
        except Exception:
            return 'UNKNOWN'  # No effect after a controller validation error.
        if decision != 'ACCEPT':
            return decision if decision in ('REJECT', 'UNKNOWN') else 'UNKNOWN'
        digest = hashlib.sha256(json.dumps(expected, sort_keys=True).encode()).hexdigest()
        with connect(self.path) as db:
            db.execute('BEGIN IMMEDIATE')
            old = db.execute('SELECT digest,state FROM journal WHERE id=?', (effect_id,)).fetchone()
            if old and old[0] != digest:
                db.rollback()
                return 'CONFLICT'
            if not old:
                changed = db.execute('UPDATE budget SET remaining=remaining-1 '
                                     'WHERE id=1 AND remaining>0').rowcount
                if not changed:
                    db.rollback()
                    return 'BUDGET_EXHAUSTED'
                db.execute('INSERT INTO journal VALUES (?,?,?)', (effect_id, digest, 'PENDING'))
            db.commit()
        if crash == 'before_effect':
            raise InterruptedError('Simulated stop before effect')
        try:
            observed = destination.lookup(effect_id)
            if observed is not None and observed != digest:
                return 'CONFLICT'
            if observed is None:
                destination.apply(effect_id, digest)
        except (ConnectionError, ValueError):
            return 'UNKNOWN'  # Reservation remains spent; reconcile on recovery.
        if crash == 'after_effect':
            raise InterruptedError('Simulated response lost before acknowledgement')
        with connect(self.path) as db:
            db.execute('UPDATE journal SET state=? WHERE id=? AND digest=?',
                       ('ACKNOWLEDGED', effect_id, digest))
        return 'ACCEPTED'


class ControlChecks(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        self.controller = Controller(root/'controller.db', 2)
        self.destination = Destination(root/'destination.db')
        self.expected = dict(producer='fixture-checker', version='1', run='run-1',
                             revision='commit-a+worktree-digest-a', scope='synthetic-change')
        self.receipt = dict(self.expected, status='SUCCEEDED', decision='ACCEPT',
                            expires=200, complete=True)

    def perform(self, receipt=None, **kwargs):
        return self.controller.perform(json.dumps(self.receipt if receipt is None else receipt),
                                       self.expected, 100, 'effect-1', self.destination, **kwargs)

    def test_permitted_path_observes_one_effect(self):
        self.assertEqual(self.perform(), 'ACCEPTED')
        self.assertEqual(self.destination.count(), 1)

    def test_refusal(self):
        self.assertEqual(self.perform(dict(self.receipt, decision='REJECT')), 'REJECT')
        self.assertEqual(self.destination.count(), 0)

    def test_ambiguous_verdict_is_not_acceptance(self):
        for value in ['not approved', 'approved', '', 'UNKNOWN', 'ACCEPT REJECT', None]:
            with self.subTest(value=value):
                self.assertEqual(self.perform(dict(self.receipt, decision=value)), 'UNKNOWN')
        self.assertEqual(self.destination.count(), 0)

    def test_missing_truncated_or_wrong_shape(self):
        conflicting = '{"decision":"REJECT",' + json.dumps(self.receipt)[1:]
        for raw in ['', '{', '{}', '[]', 'null', conflicting]:
            with self.subTest(raw=raw):
                self.assertEqual(self.controller.perform(raw, self.expected, 100,
                                 'effect-1', self.destination), 'UNKNOWN')
        self.assertEqual(self.destination.count(), 0)

    def test_foreign_stale_partial_or_failed_receipt(self):
        for field,value in [('producer','impostor'), ('version','0'), ('run','other-run'),
                            ('revision','commit-b'), ('scope','other-change'), ('expires',100),
                            ('complete',False), ('complete',1), ('status','FAILED')]:
            with self.subTest(field=field):
                self.assertEqual(self.perform(dict(self.receipt, **{field:value})), 'UNKNOWN')
        self.assertEqual(self.destination.count(), 0)

    def test_changed_worktree_invalidates_old_evidence(self):
        self.expected['revision'] = 'commit-a+worktree-digest-b'
        self.assertEqual(self.perform(), 'UNKNOWN')
        self.assertEqual(self.destination.count(), 0)

    def test_control_exception_prevents_effect(self):
        def broken(*args):
            raise RuntimeError('Broken check')
        self.assertEqual(self.perform(check=broken), 'UNKNOWN')
        for value in ['ACCEPTED', 'not approved', None]:
            with self.subTest(value=value):
                self.assertEqual(self.perform(check=lambda *args: value), 'UNKNOWN')
        self.assertEqual(self.destination.count(), 0)

    def test_budget_survives_restart(self):
        raw = json.dumps(self.receipt)
        for key in ['effect-1','effect-2']:
            self.assertEqual(self.controller.perform(raw,self.expected,100,key,self.destination), 'ACCEPTED')
        restarted = Controller(self.controller.path, 999)
        self.assertEqual(restarted.remaining(), 0)
        self.assertEqual(restarted.perform(raw,self.expected,100,'effect-3',self.destination), 'BUDGET_EXHAUSTED')
        self.assertEqual(self.destination.count(), 2)

    def test_interruption_before_effect(self):
        with self.assertRaises(InterruptedError):
            self.perform(crash='before_effect')
        self.assertEqual(self.destination.count(), 0)
        self.controller = Controller(self.controller.path, 999)
        self.assertEqual(self.perform(), 'ACCEPTED')
        self.assertEqual(self.destination.count(), 1)
        self.assertEqual(self.controller.remaining(), 1)

    def test_lost_response_reconciles_without_second_effect(self):
        with self.assertRaises(InterruptedError):
            self.perform(crash='after_effect')
        self.controller = Controller(self.controller.path, 999)
        self.assertEqual(self.perform(), 'ACCEPTED')
        self.assertEqual(self.perform(), 'ACCEPTED')
        self.assertEqual(self.destination.count(), 1)
        self.assertEqual(self.controller.remaining(), 1)

    def test_unavailable_destination_stays_uncertain(self):
        self.destination.available = False
        self.assertEqual(self.perform(), 'UNKNOWN')
        self.assertEqual(self.destination.count(), 0)
        self.assertEqual(self.controller.remaining(), 1)
        self.destination.available = True
        self.assertEqual(self.perform(), 'ACCEPTED')
        self.assertEqual(self.controller.remaining(), 1)

    def test_concurrent_attempts_preserve_budget_and_effect_identity(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(lambda _: self.perform(), range(16)))
        self.assertEqual(set(results), {'ACCEPTED'})
        self.assertEqual(self.destination.count(), 1)
        self.assertEqual(self.controller.remaining(), 1)

    def test_reused_identity_cannot_overwrite_changed_content(self):
        self.assertEqual(self.perform(), 'ACCEPTED')
        self.expected['revision'] = 'commit-b'
        self.receipt['revision'] = 'commit-b'
        self.assertEqual(self.perform(), 'CONFLICT')
        self.assertEqual(self.destination.count(), 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
