"""캐시 관리 모듈 테스트"""
import os
import tempfile
import unittest
from unittest.mock import patch

from cache_manager import (
    get_cached_summary,
    save_cached_summary,
    get_cached_script,
    save_cached_script,
)


class TestCacheManager(unittest.TestCase):
    """캐시 관리 모듈 테스트 클래스"""
    
    def setUp(self):
        """테스트 전 설정"""
        self.test_article_id = "test_article_123"
        self.test_summary = "테스트 요약입니다."
        self.test_script = "TYPE=cover | HEAD=테스트"
    
    @patch("cache_manager.CACHE_DIR")
    def test_save_and_get_summary(self, mock_cache_dir):
        """요약 저장 및 조회 테스트"""
        with tempfile.TemporaryDirectory() as tmpdir:
            mock_cache_dir.return_value = tmpdir
            os.makedirs(tmpdir, exist_ok=True)
            
            # 저장
            save_cached_summary(self.test_article_id, self.test_summary)
            
            # 조회
            result = get_cached_summary(self.test_article_id)
            self.assertEqual(result, self.test_summary)
    
    @patch("cache_manager.CACHE_DIR")
    def test_save_and_get_script(self, mock_cache_dir):
        """카드뉴스 문구 저장 및 조회 테스트"""
        with tempfile.TemporaryDirectory() as tmpdir:
            mock_cache_dir.return_value = tmpdir
            os.makedirs(tmpdir, exist_ok=True)
            
            # 저장
            save_cached_script(self.test_article_id, self.test_script)
            
            # 조회
            result = get_cached_script(self.test_article_id)
            self.assertEqual(result, self.test_script)
    
    def test_get_nonexistent_summary(self):
        """존재하지 않는 요약 조회 테스트"""
        result = get_cached_summary("nonexistent_id")
        self.assertIsNone(result)
    
    def test_get_nonexistent_script(self):
        """존재하지 않는 카드뉴스 문구 조회 테스트"""
        result = get_cached_script("nonexistent_id")
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()


