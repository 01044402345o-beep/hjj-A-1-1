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


class TestFilterByKeyword(unittest.TestCase):
    def setUp(self):
        self.prompts = [
            make_prompt("블로그 글 작성", content="SEO 최적화"),
            make_prompt("썸네일 생성", content="미니멀 스타일"),
            make_prompt("요약 도우미", content="블로그 본문을 요약"),
        ]

    def test_matches_title(self):
        result = pm.filter_by_keyword(self.prompts, "썸네일")
        self.assertEqual(["썸네일 생성"], [p["title"] for p in result])

    def test_matches_content(self):
        result = pm.filter_by_keyword(self.prompts, "미니멀")
        self.assertEqual(["썸네일 생성"], [p["title"] for p in result])

    def test_matches_title_or_content(self):
        result = pm.filter_by_keyword(self.prompts, "블로그")
        self.assertEqual(["블로그 글 작성", "요약 도우미"], [p["title"] for p in result])

    def test_is_case_insensitive(self):
        result = pm.filter_by_keyword(self.prompts, "seo")
        self.assertEqual(["블로그 글 작성"], [p["title"] for p in result])

    def test_returns_empty_for_no_match(self):
        self.assertEqual([], pm.filter_by_keyword(self.prompts, "존재하지않음"))

    def test_returns_empty_for_blank_keyword(self):
        self.assertEqual([], pm.filter_by_keyword(self.prompts, "   "))


class TestFilterFavorites(unittest.TestCase):
    def test_returns_only_favorites(self):
        prompts = [
            make_prompt("A", favorite=True),
            make_prompt("B", favorite=False),
            make_prompt("C", favorite=True),
        ]
        result = pm.filter_favorites(prompts)
        self.assertEqual(["A", "C"], [p["title"] for p in result])

    def test_returns_empty_when_none_favorited(self):
        prompts = [make_prompt("A"), make_prompt("B")]
        self.assertEqual([], pm.filter_favorites(prompts))

    def test_returns_empty_for_empty_input(self):
        self.assertEqual([], pm.filter_favorites([]))


if __name__ == "__main__":
    unittest.main()
