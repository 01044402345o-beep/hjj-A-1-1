"""prompt_manager의 순수 로직 함수 테스트."""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import prompt_manager as pm


def make_prompt(title, content="내용", category="기타", favorite=False):
    return {
        "title": title,
        "content": content,
        "category": category,
        "favorite": favorite,
    }


class TestFilterByCategory(unittest.TestCase):
    def setUp(self):
        self.prompts = [
            make_prompt("A", category="텍스트 생성"),
            make_prompt("B", category="이미지 생성"),
            make_prompt("C", category="텍스트 생성"),
        ]

    def test_returns_only_matching_category(self):
        result = pm.filter_by_category(self.prompts, "텍스트 생성")
        self.assertEqual(["A", "C"], [p["title"] for p in result])

    def test_returns_empty_when_no_match(self):
        self.assertEqual([], pm.filter_by_category(self.prompts, "자동화"))

    def test_preserves_original_order(self):
        result = pm.filter_by_category(self.prompts, "텍스트 생성")
        self.assertIs(self.prompts[0], result[0])

    def test_does_not_mutate_input(self):
        pm.filter_by_category(self.prompts, "텍스트 생성")
        self.assertEqual(3, len(self.prompts))


if __name__ == "__main__":
    unittest.main()
