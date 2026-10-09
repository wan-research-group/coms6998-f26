"""Student slides stay attached to their required paper and named presenters."""
import unittest
import re
from pathlib import Path
from zipfile import ZipFile

import build


class PaperPresentationsTest(unittest.TestCase):
    def test_homepage_presentations_match_each_paper_and_week(self):
        glance = build.glance_html()
        self.assertEqual(glance.count('class="glance-presenters"'), 5)
        for week in build.weeks:
            for paper in week.get('papers', []):
                if not paper.get('presentation_slides'):
                    continue
                row = next(row for row in re.findall(r'<tr>.*?</tr>', glance, re.S)
                           if f'schedule.html#week-{week["week"]}"' in row)
                line = next(line for line in re.findall(r'<span class="glance-reading">.*?</span></span>', row)
                            if paper['presentation_slides'] in line)
                self.assertIn(paper['short_title'], line)
                for name in paper['presenters']:
                    self.assertIn(name, line)
                self.assertIn(f'href="{paper["presentation_slides"]}"', line)

    def test_paper_presenters_and_assets(self):
        expected = {
            (3, 'PagedAttention'): ['Aaron Cherian'],
            (3, 'SGLang'): ['Gavin Zou', 'Pingchuan Dong'],
            (4, 'TPU'): ['Lizhong Wang', 'Jiangrui Xu'],
            (4, 'Open AI Jalapeño Chip'): ['Shen Li', 'Yichen Xu'],
            (5, 'Embodied.cpp'): ['Ryan Ma', 'George Wang'],
        }
        roster = {s['name'] for s in build.students}
        found = {}
        for week in build.weeks:
            for paper in week.get('papers', []):
                if not paper.get('presentation_slides'):
                    continue
                found[week['week'], paper['short_title']] = paper['presenters']
                self.assertTrue(set(paper['presenters']) <= roster)
                path = Path(paper['presentation_slides'])
                self.assertEqual(path.parent.as_posix(), 'assets/slides/students')
                self.assertNotRegex(path.name, r'LATE|\d{6,}')
                with ZipFile(build.ROOT / path) as deck:
                    self.assertIsNone(deck.testzip())
                item = build.paper_li(paper, 'req')
                self.assertIn(f'href="{path.as_posix()}"', item)
                for name in paper['presenters']:
                    self.assertIn(name, item)
                self.assertIn(path.as_posix(), build.syllabus_markdown())
        self.assertEqual(found, expected)

    def test_unsubmitted_papers_have_no_placeholder(self):
        for week in build.weeks:
            for paper in week.get('papers', []):
                if not paper.get('presentation_slides'):
                    self.assertNotIn('paper-presentation', build.paper_li(paper, 'req'))


if __name__ == '__main__':
    unittest.main()
