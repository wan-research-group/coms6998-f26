"""Student slides stay attached to their required paper and named presenters."""
import unittest
import re
from pathlib import Path
from zipfile import ZipFile
from unittest.mock import patch

import build


class PaperPresentationsTest(unittest.TestCase):
    def test_homepage_presentations_match_each_paper_and_week(self):
        glance = build.glance_html()
        self.assertEqual(glance.count('class="glance-presenters"'), 21)
        for week in build.weeks:
            for paper in week.get('papers', []):
                if not paper.get('presentation_slides'):
                    continue
                row = next(row for row in re.findall(r'<tr>.*?</tr>', glance, re.S)
                           if f'schedule.html#week-{week["week"]}"' in row)
                downloads = build.presentation_slide_links(paper, compact=True)
                line = next(line for line in re.findall(r'<span class="glance-reading">.*?</span></span>', row)
                            if downloads[0][0] in line)
                self.assertIn(paper['short_title'], line)
                for name in paper['presenters']:
                    self.assertIn(name, line)
                for url, label in downloads:
                    self.assertIn(f'href="{url}"', line)
                    self.assertIn(label, line)

    def test_paper_presenters_and_assets(self):
        expected = {
            (3, 'PagedAttention'): ['Aaron Cherian'],
            (3, 'SGLang'): ['Gavin Zou', 'Pingchuan Dong'],
            (4, 'TPU'): ['Lizhong Wang', 'Jiangrui Xu'],
            (4, 'Open AI Jalapeño Chip'): ['Shen Li', 'Yichen Xu'],
            (5, 'Embodied.cpp'): ['Ryan Ma', 'George Wang'],
            (5, 'VLA-Perf'): ['Shiyao Marcus Lam', 'Pulak Mehrotra'],
            (6, 'ReCA'): ['Yishan Song', 'Shurui Hu'],
            (7, 'CogSys'): ['Vayun Gupta'],
            (7, 'Lobster'): ['Dakshinamoorthy Amirthaganesan'],
            (8, 'AlphaDev'): ['Baichuan Xiang', 'Zixin (Stan) Wan'],
            (8, 'AlphaEvolve'): ['Lei Chi'],
            (8, 'KernelBench'): ['Mingkai Li', 'Shufeng Chen'],
        }
        roster = {s['name'] for s in build.students}
        found = {}
        for week in build.weeks:
            for paper in week.get('papers', []):
                if not paper.get('presentation_slides'):
                    continue
                found[week['week'], paper['short_title']] = paper['presenters']
                roster_names = {'Shiyao Marcus Lam': 'Marcus Lam'}
                self.assertTrue({roster_names.get(name, name) for name in paper['presenters']} <= roster)
                item = build.paper_li(paper, 'req')
                for url, label in build.presentation_slide_links(paper):
                    path = Path(url)
                    self.assertEqual(path.parent.as_posix(), 'assets/slides/students')
                    self.assertNotRegex(path.name, r'LATE|\d{6,}')
                    if path.suffix == '.pptx':
                        with ZipFile(build.ROOT / path) as deck:
                            self.assertIsNone(deck.testzip())
                    else:
                        self.assertEqual(path.suffix, '.pdf')
                        self.assertTrue((build.ROOT / path).read_bytes().startswith(b'%PDF-'))
                    self.assertIn(label, item)
                    self.assertIn(f'href="{url}"', item)
                    self.assertIn(url, build.syllabus_markdown())
                for name in paper['presenters']:
                    self.assertIn(name, item)
        self.assertEqual(found, expected)

    def test_unsubmitted_papers_have_no_placeholder(self):
        for week in build.weeks:
            for paper in week.get('papers', []):
                if not paper.get('presenters'):
                    self.assertNotIn('paper-presentation', build.paper_li(paper, 'req'))

    def test_presenters_without_slides(self):
        paper = next(p for w in build.weeks for p in w.get('papers', [])
                     if p.get('short_title') == 'VLA-Perf')
        paper = dict(paper)
        paper.pop('presentation_slides')
        self.assertEqual(paper['presenters'], ['Shiyao Marcus Lam', 'Pulak Mehrotra'])
        self.assertNotIn('presentation_slides', paper)
        item = build.paper_li(paper, 'req')
        self.assertIn('Presenters: Shiyao Marcus Lam, Pulak Mehrotra', item)
        self.assertNotIn('Presentation slides', item)
        week = next(w for w in build.weeks if w['week'] == 5)
        with patch.object(build, 'weeks', [dict(week, papers=[paper])]):
            glance = build.glance_html()
        line = next(line for line in re.findall(r'<span class="glance-reading">.*?</span></span>', glance)
                    if 'VLA-Perf' in line)
        self.assertIn('Shiyao Marcus Lam, Pulak Mehrotra', line)
        self.assertNotIn('Slides (PPTX)', line)
        self.assertIn('Presenters: Shiyao Marcus Lam, Pulak Mehrotra', build.syllabus_markdown())

    def test_vla_perf_pdf_labels(self):
        paper = next(p for w in build.weeks for p in w.get('papers', [])
                     if p.get('short_title') == 'VLA-Perf')
        self.assertEqual(build.presentation_format(paper), 'PDF')
        line = next(line for line in re.findall(r'<span class="glance-reading">.*?</span></span>', build.glance_html())
                    if 'VLA-Perf' in line)
        self.assertIn('Slides (PDF)', line)
        self.assertNotIn('PPTX', line)
        self.assertIn(f"[Presentation slides (PDF)]({paper['presentation_slides']})", build.syllabus_markdown())

    def test_week_six_and_seven_presenter_assignments(self):
        expected = {
            (6, 'ReCA'): ['Yishan Song', 'Shurui Hu'],
            (6, 'DiTPA'): ['Wenjuan Zheng'],
            (7, 'CogSys'): ['Vayun Gupta'],
            (7, 'REASON'): ['Charlotte Chen'],
            (7, 'Lobster'): ['Dakshinamoorthy Amirthaganesan'],
        }
        roster = {s['name'] for s in build.students}
        glance = build.glance_html()
        for (week_num, title), names in expected.items():
            week = next(w for w in build.weeks if w['week'] == week_num)
            paper = next(p for p in week['papers'] if p['short_title'] == title)
            self.assertEqual(paper['presenters'], names)
            self.assertTrue(set(names) <= roster)
            downloads = {
                'ReCA': 'assets/slides/students/week06-reca-yishan-song-shurui-hu.pdf',
                'CogSys': 'assets/slides/students/week07-cogsys-vayun-gupta.pptx',
                'Lobster': 'assets/slides/students/week07-lobster-dakshinamoorthy-amirthaganesan.pptx',
            }
            if title in downloads:
                self.assertEqual(paper['presentation_slides'], downloads[title])
            else:
                self.assertNotIn('presentation_slides', paper)
            row = next(row for row in re.findall(r'<tr>.*?</tr>', glance, re.S)
                       if f'schedule.html#week-{week_num}"' in row)
            line = next(line for line in re.findall(r'<span class="glance-reading">.*?</span></span>', row)
                        if f'>{title}</a>' in line)
            for name in names:
                self.assertIn(name, line)
                self.assertIn(name, build.paper_li(paper, 'req'))
                self.assertIn(name, build.syllabus_markdown())
            if title in downloads:
                self.assertIn('Slides (PDF)' if title == 'ReCA' else 'Slides (PPTX)', line)
                self.assertIn(paper['presentation_slides'], line)
            else:
                self.assertNotIn('Slides (', line)

    def test_alphadev_parts_have_distinct_ordered_download_links(self):
        paper = next(p for w in build.weeks for p in w.get('papers', [])
                     if p.get('short_title') == 'AlphaDev')
        urls = [
            'assets/slides/students/week08-alphadev-part1-baichuan-xiang.pptx',
            'assets/slides/students/week08-alphadev-part2-zixin-wan.pptx',
        ]
        self.assertEqual(paper['presentation_slides'], urls)
        full_labels = ['Presentation slides, Part 1 (PPTX)', 'Presentation slides, Part 2 (PPTX)']
        compact_labels = ['Slides, Part 1 (PPTX)', 'Slides, Part 2 (PPTX)']
        self.assertEqual(build.presentation_slide_links(paper), list(zip(urls, full_labels)))
        self.assertEqual(build.presentation_slide_links(paper, compact=True),
                         list(zip(urls, compact_labels)))
        item = build.paper_li(paper, 'req')
        glance = build.glance_html()
        syllabus = build.syllabus_markdown()
        for url, full, compact in zip(urls, full_labels, compact_labels):
            self.assertIn(f'href="{url}"', item)
            self.assertIn(full, item)
            self.assertIn(f'href="{url}"', glance)
            self.assertIn(compact, glance)
            self.assertIn(f'[{full}]({url})', syllabus)
        for rendered in (item, glance, syllabus):
            self.assertLess(rendered.index(urls[0]), rendered.index(urls[1]))


if __name__ == '__main__':
    unittest.main()
