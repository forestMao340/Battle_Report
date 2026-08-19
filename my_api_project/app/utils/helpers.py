import re

def detect_source_lang(text: str) -> str:
    """简单检测文本是否含中文"""
    return "zh" if re.search(r'[\u4e00-\u9fff]', text) else "en"