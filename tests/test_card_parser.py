"""카드뉴스 파서 테스트"""
import unittest

from card_parser import parse_card_script


class TestCardParser(unittest.TestCase):
    """카드뉴스 파서 테스트 클래스"""
    
    def test_parse_valid_script(self):
        """유효한 카드뉴스 문구 파싱 테스트"""
        script = """1. TYPE=cover | HEAD=테스트 제목 | IMAGE_KEY=test keyword
2. TYPE=program | HEAD=프로그램 제목 | BODY=프로그램 본문 | IMAGE_KEY=program keyword"""
        
        cards = parse_card_script(script)
        
        self.assertEqual(len(cards), 2)
        self.assertEqual(cards[0]["type"], "cover")
        self.assertEqual(cards[0]["head"], "테스트 제목")
        self.assertEqual(cards[1]["type"], "program")
        self.assertEqual(cards[1]["body"], "프로그램 본문")
    
    def test_parse_empty_script(self):
        """빈 스크립트 파싱 테스트"""
        cards = parse_card_script("")
        self.assertEqual(len(cards), 0)
    
    def test_parse_invalid_format(self):
        """잘못된 형식 파싱 테스트"""
        script = "이것은 유효하지 않은 형식입니다."
        cards = parse_card_script(script)
        self.assertEqual(len(cards), 0)


if __name__ == "__main__":
    unittest.main()


