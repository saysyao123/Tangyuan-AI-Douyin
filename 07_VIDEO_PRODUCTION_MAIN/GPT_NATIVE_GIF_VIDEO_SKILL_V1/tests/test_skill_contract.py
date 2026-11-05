"""Check workflow integrity without pretending repository layout is installed."""
from pathlib import Path
import re
import unittest

ROOT=Path(__file__).resolve().parents[1]


class SkillContractTests(unittest.TestCase):
    def test_frontmatter_uses_standard_minimal_fields(self):
        text=(ROOT/'SKILL.md').read_text(encoding='utf-8')
        front=text.split('---',2)[1]
        fields=dict(line.split(':',1) for line in front.strip().splitlines())
        self.assertEqual(set(fields),{'name','description'})
        self.assertRegex(fields['name'].strip(),r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
        self.assertLessEqual(len(fields['name'].strip()),64)
        self.assertLessEqual(len(fields['description'].strip()),1024)

    def test_repository_layout_installation_gap_is_disclosed(self):
        start=(ROOT/'START_WEB.md').read_text(encoding='utf-8')
        self.assertIn('不是严格可安装',start)
        self.assertIn('没有在 ChatGPT 全局安装',start)
        self.assertIn('同一 SHA',start)

    def test_referenced_local_resources_exist(self):
        text=(ROOT/'SKILL.md').read_text(encoding='utf-8')
        for link in re.findall(r'\]\(([^)]+)\)',text):
            if '://' not in link:self.assertTrue((ROOT/link).is_file(),link)

    def test_parent_router_keeps_work_fisher_priority(self):
        text=(ROOT.parent/'README.md').read_text(encoding='utf-8')
        self.assertIn('当前默认 Work-Fisher',text)
        self.assertIn('不改变上述 Work-Fisher',text)


if __name__=='__main__':unittest.main()
