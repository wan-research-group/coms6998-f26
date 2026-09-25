"""Student profiles retain placeholders and support supplied photos and links."""

import pathlib
import hashlib
import unittest
from unittest.mock import patch
from urllib.parse import urlsplit

import build


class StudentsTest(unittest.TestCase):
    def test_stylesheet_cache_version(self):
        version = hashlib.sha256((build.ROOT / "assets/style.css").read_bytes()).hexdigest()[:12]
        page = build.page(title="Students", description="Students", body=build.students_body(), path="students.html")
        self.assertIn(f'href="assets/style.css?v={version}"', page)

    def test_profiles_and_placeholders(self):
        profiles = [
            {"name": "Jane Middle Doe", "photo": "assets/students/jane_photo.jpg", "photo_position": "50% 0%",
             "link": "https://example.com/", "email": "jane@example.com"},
            {"name": "John Roe"},
        ]
        with patch.object(build, "students", profiles):
            page = build.students_body()
        self.assertIn('src="assets/students/jane_photo.jpg"', page)
        self.assertIn('style="object-position: 50% 0%"', page)
        self.assertIn('href="https://example.com/"', page)
        self.assertIn('<span class="stu-name">Jane Middle Doe</span>', page)
        self.assertIn('<span class="stu-name">John Roe</span>', page)
        self.assertNotIn('<span class="stu-name"><a', page)
        self.assertIn('aria-label="Jane Middle Doe: profile (opens in a new tab)"', page)
        self.assertIn('aria-hidden="true" focusable="false"', page)
        self.assertIn('aria-hidden="true">JR</span>', page)
        self.assertEqual(page.count('class="stu-card"'), 2)
        self.assertEqual(page.count('class="stu-profile"'), 1)
        self.assertEqual(page.count('class="stu-email"'), 1)
        self.assertEqual(page.count('class="stu-contacts"'), 1)
        self.assertIn('href="mailto:jane@example.com"', page)
        self.assertIn('aria-label="Email Jane Middle Doe: jane@example.com"', page)
        self.assertEqual(build.initials("Jane Middle Doe"), "JD")

    def test_roster_and_local_photo_references(self):
        names = [s["name"] for s in build.students]
        self.assertEqual(len(names), len(set(names)))
        self.assertEqual(names, sorted(names, key=lambda n: (
            n.rsplit(" ", 1)[-1].casefold(), n.rsplit(" ", 1)[0].casefold())))
        for student in build.students:
            self.assertLessEqual(set(student), {"name", "photo", "photo_position", "link", "email"})
            self.assertRegex(student["email"], r'^[A-Za-z0-9._+-]+@columbia\.edu$')
            if student.get("photo"):
                path = pathlib.Path(student["photo"])
                self.assertEqual(path.parent.as_posix(), "assets/students")
                self.assertEqual(path.name, student["name"] + "_photo.jpg")
                self.assertTrue((build.ROOT / path).is_file())
            urls = ([student["link"]] if student.get("link") else [])
            for url in urls:
                self.assertEqual(urlsplit(url).scheme, "https")
                self.assertTrue(urlsplit(url).netloc)
        page = build.students_body()
        self.assertEqual(page.count('class="stu-profile"'), sum(bool(s.get("link")) for s in build.students))
        self.assertNotIn('<span class="stu-name"><a', page)
        zihao = next(s for s in build.students if s["name"] == "Zihao Fang")
        self.assertEqual(zihao["link"], "https://fzhwenzhou.github.io/")
        self.assertNotIn('https://github.com/fzhwenzhou', page)
        self.assertEqual(page.count('class="stu-email"'), len(build.students))
        self.assertEqual(page.count('class="stu-contacts"'), len(build.students))
        for student in build.students:
            self.assertIn(f'href="mailto:{student["email"]}"', page)
        self.assertNotRegex(page, r'\bC\d{9}\b')

    def test_email_only_student(self):
        with patch.object(build, "students", [{"name": "John Roe", "email": "john@example.com"}]):
            page = build.students_body()
        self.assertIn('href="mailto:john@example.com"', page)
        self.assertIn('aria-hidden="true">JR</span>', page)
        self.assertIn('<span class="stu-name">John Roe</span>', page)
        self.assertNotIn('class="stu-profile"', page)


if __name__ == "__main__":
    unittest.main()
