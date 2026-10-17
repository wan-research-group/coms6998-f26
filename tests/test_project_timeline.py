"""Keep project milestones and weekly deadline listings consistent."""
import datetime as dt
import unittest

import build


class ProjectTimelineTest(unittest.TestCase):
    def test_milestone_dates_and_order(self):
        dates = {m['id']: m['date'] for m in build.milestones}
        self.assertEqual(dates, {
            'Proposal': dt.date(2026, 10, 5),
            'P1': dt.date(2026, 10, 26),
            'Midterm': dt.date(2026, 11, 6),
            'P2': dt.date(2026, 11, 9),
            'P3': dt.date(2026, 11, 23),
            'P4': dt.date(2026, 12, 7),
            'Poster': dt.date(2026, 12, 11),
            'Final': dt.date(2026, 12, 18),
        })
        self.assertEqual(list(dates.values()), sorted(dates.values()))

    def test_weekly_deadlines_and_rendered_dates(self):
        weeks = {w['week']: w for w in build.weeks}
        self.assertEqual(weeks[7]['deadlines'], ['Oct 26, 11:59 PM - P1 exploration & progress'])
        self.assertEqual(weeks[9]['deadlines'], [
            'Nov 5, 11:59 PM - midterm slides',
            'Nov 9, 11:59 PM - P2 prototype & pilot results',
        ])
        self.assertFalse(weeks[6].get('deadlines'))
        self.assertFalse(weeks[8].get('deadlines'))
        for page in (build.glance_html(), build.now_html(), build.schedule_body(),
                     build.project_body(), build.syllabus_markdown()):
            self.assertIn('Oct 26', page)
            self.assertIn('Nov 9', page)
            self.assertNotIn('Oct 19', page)
            self.assertNotIn('Nov 2,', page)
        self.assertIn('incorporate class feedback', build.schedule_body())


if __name__ == '__main__':
    unittest.main()
