/* Dependency-free tests for disclosure links, printing, and deadline visibility. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const source = fs.readFileSync(path.join(__dirname, '../assets/site.js'), 'utf8');

function harness(hash = '') {
  const events = {};
  const outer = {tagName: 'DETAILS', open: false, parentElement: null};
  const inner = {tagName: 'DETAILS', open: false, parentElement: outer};
  const existing = {tagName: 'DETAILS', open: true, parentElement: null};
  const target = {
    parentElement: inner,
    matches: selector => selector === '.candidate, .project-idea',
    scrollIntoView: () => { target.scrolled = true; },
  };
  const window = {
    location: {hash},
    addEventListener: (name, handler) => { (events[name] ||= []).push(handler); },
  };
  const document = {
    documentElement: {},
    getElementById: id => id === 'project-test' ? target : null,
    querySelector: () => null,
    querySelectorAll: selector => {
      assert.ok(selector.includes('details.project-ideas:not([open])'));
      assert.ok(selector.includes('details.project-brief:not([open])'));
      return [outer, inner, existing].filter(d => !d.open);
    },
  };
  vm.runInNewContext(source, {document, window, decodeURIComponent});
  return {outer, inner, existing, target, window, fire: name => events[name].forEach(f => f())};
}

const linked = harness('#project-test');
assert.equal(linked.outer.open, true);
assert.equal(linked.inner.open, true);
assert.equal(linked.target.scrolled, true);

const changed = harness();
changed.window.location.hash = '#project-test';
changed.fire('hashchange');
assert.equal(changed.outer.open, true);
assert.equal(changed.inner.open, true);

const printed = harness();
printed.fire('beforeprint');
assert.ok(printed.outer.open && printed.inner.open && printed.existing.open);
printed.fire('afterprint');
assert.equal(printed.outer.open, false);
assert.equal(printed.inner.open, false);
assert.equal(printed.existing.open, true);

assert.doesNotThrow(() => harness('#%invalid'));
console.log('PASS: initial/hash-change links reveal nested briefs; printing restores prior disclosure state.');

function nowHarness(moment) {
  class FixedDate extends Date {
    constructor(...args) {
      super(...(args.length ? args : [moment]));
    }
    static now() { return new Date(moment).getTime(); }
  }

  const deadlines = [
    {id: 'p1', due: '2026-10-26T23:59:00-04:00', week: '7'},
    {id: 'midterm-slides', due: '2026-11-05T23:59:00-05:00', week: '9'},
    {id: 'p2', due: '2026-11-09T23:59:00-05:00', week: '9'},
    {id: 'p3', due: '2026-11-23T23:59:00-05:00', week: '11'},
    {id: 'final', due: '2026-12-18T23:59:00-05:00', week: '13'},
  ].map(record => ({
    ...record,
    hidden: false,
    getAttribute: name => ({'data-due': record.due, 'data-week': record.week})[name] ?? null,
  }));
  const emptyState = {hidden: true};
  const nowSection = {
    querySelectorAll: selector => {
      if (selector.startsWith('.now-class')) return [];
      if (selector.startsWith('.now-deadline-item')) return deadlines;
      throw new Error(`Unexpected Now selector: ${selector}`);
    },
  };
  const document = {
    documentElement: {},
    getElementById: id => id === 'now' ? nowSection : (id === 'now-no-deadline' ? emptyState : null),
    querySelector: () => null,
    querySelectorAll: () => [],
  };
  const window = {location: {hash: ''}, addEventListener: () => {}};
  vm.runInNewContext(source, {document, window, Date: FixedDate, decodeURIComponent});
  return {
    visible: deadlines.filter(item => !item.hidden).map(item => item.id),
    empty: !emptyState.hidden,
  };
}

assert.deepEqual(nowHarness('2026-11-01T12:00:00-05:00'), {
  visible: ['midterm-slides', 'p2'], empty: false,
});
assert.deepEqual(nowHarness('2026-11-05T23:59:00-05:00'), {
  visible: ['midterm-slides', 'p2'], empty: false,
});
assert.deepEqual(nowHarness('2026-11-05T23:59:00.001-05:00'), {
  visible: ['p2'], empty: false,
});
assert.deepEqual(nowHarness('2026-11-06T12:00:00-05:00'), {
  visible: ['p2'], empty: false,
});
assert.deepEqual(nowHarness('2026-11-10T12:00:00-05:00'), {
  visible: ['p3'], empty: false,
});
assert.deepEqual(nowHarness('2026-12-19T12:00:00-05:00'), {
  visible: [], empty: true,
});
console.log('PASS: Now shows upcoming deadlines from the nearest deadline week and expires them at the correct instant.');
