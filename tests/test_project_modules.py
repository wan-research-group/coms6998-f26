"""Regression checks for the six-module project guide (no browser dependencies)."""

import html
import re
import unittest
from collections import Counter

import build


class ProjectModulesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.page = build.project_body()
        cls.syllabus = build.syllabus_markdown()

    def test_six_modules_and_all_briefs_assigned_once(self):
        modules = build.project_modules
        self.assertEqual([m["number"] for m in modules], list(range(1, 7)))
        self.assertEqual([len(m["ideas"]) for m in modules], [4, 5, 4, 4, 4, 5])
        self.assertEqual(Counter(m["track"] for m in modules), {
            "computing-for-ai": 3, "ai-for-computing": 3,
        })
        references = [name for m in modules for idea in m["ideas"] for name in idea["briefs"]]
        self.assertEqual(len(references), 26)
        self.assertEqual(Counter(references), Counter(build.project_briefs.keys()))
        self.assertEqual(self.page.count('class="project-ideas"'), 6)
        self.assertEqual(self.page.count('class="project-idea"'), 26)
        self.assertEqual(self.page.count('class="candidate"'), 26)
        self.assertNotRegex(self.page, r'<details[^>]*\sopen(?:\s|=|>)')

    def test_guide_content_and_briefs_are_complete(self):
        for module in build.project_modules:
            for key in ["title", "overview", "background", "success"]:
                self.assertIn(html.escape(module[key], quote=True), self.page)
                self.assertIn(module[key], self.syllabus)
            for idea in module["ideas"]:
                self.assertIn(html.escape(idea["title"], quote=True), self.page)
                self.assertIn(html.escape(idea["description"], quote=True), self.page)
                self.assertIn(idea["description"], self.syllabus)
        for name, brief in build.project_briefs.items():
            for value in brief.values():
                self.assertIn(html.escape(value, quote=True), self.page)
            self.assertIn(f'project.html#project-{name.lower()}', self.syllabus)

    def test_anchors_hierarchy_and_placement(self):
        ids = re.findall(r'\bid="([^"]+)"', self.page)
        self.assertEqual(len(ids), len(set(ids)))
        for anchor in re.findall(r'href="#([^"]+)"', self.page):
            self.assertIn(anchor, ids)
        for name in build.project_briefs:
            self.assertIn(f'project-{name.lower()}', ids)
        headings = [int(level) for level in re.findall(r'<h([1-6])\b', self.page)]
        self.assertTrue(all(b <= a + 1 for a, b in zip(headings, headings[1:])))
        self.assertLess(self.page.index('id="final-submission"'), self.page.index('id="directions"'))
        self.assertIn('id="computing-for-ai"', self.page)
        self.assertIn('id="ai-for-computing"', self.page)

    def test_key_scope_and_assignments(self):
        by_number = {m["number"]: m for m in build.project_modules}
        isa = next(idea for idea in by_number[5]["ideas"] if "ISABenefit" in idea["briefs"])
        self.assertEqual(isa["title"], "Workload-driven ISA and accelerator extensions")
        self.assertTrue(any(i["title"] == "Efficient compositional inference" for i in by_number[3]["ideas"]))
        analog = by_number[6]["ideas"][-1]
        self.assertEqual(analog["title"], "Analog and mixed-signal circuit optimization")
        self.assertIn("fixed topology", analog["description"])
        self.assertIn("one principal mechanism", by_number[2]["scope_note"])
        self.assertIn("each team member's contribution", build.project_guide["choosing"][-1])


if __name__ == "__main__":
    unittest.main()
