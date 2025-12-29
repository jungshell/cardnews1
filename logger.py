"""로깅 시스템 모듈"""
import logging
import os
from datetime import datetime
from typing import Optional


LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, f"app_{datetime.now().strftime('%Y%m%d')}.log")
ERROR_LOG_FILE = os.path.join(LOG_DIR, f"error_{datetime.now().strftime('%Y%m%d')}.log")


def setup_logger(name: str = "cardnews", level: int = logging.INFO) -> logging.Logger:
    """
    로거를 설정하고 반환합니다.
    
    Args:
        name: 로거 이름
        level: 로그 레벨
        
    Returns:
        설정된 로거 인스턴스
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # 기존 핸들러 제거 (중복 방지)
    if logger.handlers:
        return logger
    
    # 포맷터 설정
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # 파일 핸들러 (일반 로그)
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # 파일 핸들러 (에러 로그)
    error_handler = logging.FileHandler(ERROR_LOG_FILE, encoding="utf-8")
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    logger.addHandler(error_handler)
    
    # 콘솔 핸들러
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger


# 전역 로거 인스턴스
logger = setup_logger()


