"""Guest readings and access-restricted lecture links remain distinct."""
import html
import unittest

import build


class GuestMaterialsTest(unittest.TestCase):
    def setUp(self):
        self.week = next(w for w in build.weeks if w['week'] == 6)

    def test_courseworks_slides_without_access_notice(self):
        url = 'https://courseworks2.columbia.edu/courses/258448/files/folder/Lecture%20Slides?preview=28705076'
        self.assertEqual(self.week['slides'], url)
        for page in (build.slides_html(self.week), build.glance_html(), build.now_html(),
                     build.schedule_body(), build.syllabus_markdown()):
            self.assertIn(url, html.unescape(page))
            self.assertIn('Lecture slides (CourseWorks)', page)
            self.assertNotIn('Access restricted to students enrolled in this course.', page)
        self.assertNotIn('(PDF)', build.slides_html(self.week))

    def test_guest_readings_are_separate(self):
        self.assertEqual([p['short_title'] for p in self.week['papers']], ['ReCA', 'DiTPA'])
        readings = self.week['guest_readings']
        self.assertEqual([p['url'].rsplit('/', 1)[-1] for p in readings],
                         ['7544261', '9256819', '10454572'])
        for page in (build.schedule_body(), build.papers_body(), build.syllabus_markdown()):
            self.assertIn('Guest lecture readings', page)
            for paper in readings:
                self.assertIn(paper['title'], html.unescape(page))
                self.assertIn(paper['url'], page)
        self.assertIn('href="schedule.html#guest-readings-week-6"', build.glance_html())
        self.assertIn('id="guest-readings-week-6"', build.schedule_body())

    def test_public_slide_labels_unchanged(self):
        week = next(w for w in build.weeks if w['week'] == 5)
        self.assertIn('Lecture slides (PDF)', build.slides_html(week))
        self.assertNotIn('restricted', build.slides_html(week))

    def test_guest_readings_use_short_titles(self):
        for page in (build.glance_html(), build.guest_readings_html(self.week)):
            for paper in self.week['guest_readings']:
                self.assertIn(f'>{paper["short_title"]}</a>', page)
                self.assertIn(f'title="{html.escape(paper["title"], quote=True)}"', page)
                self.assertNotIn(f'>{paper["title"]}</a>', page)
        required = self.week['papers'][0]
        self.assertIn(f'>{required["title"]}</a>', build.paper_li(required, 'req'))


if __name__ == '__main__':
    unittest.main()
