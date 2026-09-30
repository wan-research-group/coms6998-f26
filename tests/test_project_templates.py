"""Check downloadable proposal assets and links without a TeX dependency."""

import unittest
from zipfile import ZipFile

import build


class ProjectTemplatesTest(unittest.TestCase):
    def test_proposal_downloads_are_linked_and_present(self):
        proposal = next(m for m in build.milestones if m['id'] == 'Proposal')
        page = build.project_body()
        syllabus = build.syllabus_markdown()
        for field in ('template_url', 'template_preview_url'):
            url = proposal[field]
            self.assertTrue((build.ROOT / url).is_file())
            self.assertIn(f'href="{url}"', page)
            self.assertIn(f']({url})', syllabus)
        self.assertIn('LaTeX template (ZIP)', page)
        self.assertIn('PDF preview', page)
        self.assertTrue((build.ROOT / proposal['template_preview_url']).read_bytes().startswith(b'%PDF-'))

    def test_zip_matches_editable_sources(self):
        proposal = next(m for m in build.milestones if m['id'] == 'Proposal')
        sources = build.ROOT / 'templates/project-proposal'
        expected = {'main.tex', 'references.bib', 'IEEEtran.cls', 'IEEEtran_HOWTO.pdf', 'README.md'}
        with ZipFile(build.ROOT / proposal['template_url']) as archive:
            self.assertIsNone(archive.testzip())
            self.assertEqual(set(archive.namelist()), expected)
            for name in expected:
                self.assertEqual(archive.read(name), (sources / name).read_bytes())


if __name__ == '__main__':
    unittest.main()
