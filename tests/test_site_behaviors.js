/* Dependency-free tests for disclosure links and print restoration. */
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
