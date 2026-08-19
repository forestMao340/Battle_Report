from app.services.ai_client import call_deepseek, call_deepseek_stream

async def translate_text(text: str, target_lang: str) -> str:
    system_prompt = "你是一个专业的翻译助手。请将用户输入的文本翻译成指定的目标语言。只输出翻译结果，不要附加任何解释。"
    user_prompt = f"请将以下文本翻译成 {target_lang}：\n\n{text}"
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    return await call_deepseek(messages, temperature=0.3)

async def translate_text_stream(text: str, target_lang: str):
    """
    异步生成器，流式返回翻译结果。
    """
    system_prompt = "你是一个专业的翻译助手。请将用户输入的文本翻译成指定的目标语言。只输出翻译结果，不要附加任何解释。"
    user_prompt = f"请将以下文本翻译成 {target_lang}：\n\n{text}"
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    async for chunk in call_deepseek_stream(messages, temperature=0.3):
        yield chunk

async def translate_classical(text: str) -> str:
    system_prompt = "你是一位文言文翻译专家，将文言文翻译成现代白话文，保留意境。只输出翻译结果。"
    user_prompt = f"请将以下文言文翻译成现代白话文：\n\n{text}"
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    return await call_deepseek(messages, temperature=0.4, max_tokens=2048)

async def translate_classical_stream(text: str):
    """
    异步生成器，流式返回文言文→白话文翻译。
    """
    system_prompt = "你是一位精通中国古代文言文的翻译专家。将文言文翻译成现代白话文，保留原文意境和语气。只输出翻译结果。"
    user_prompt = f"请将以下文言文翻译成现代白话文：\n\n{text}"
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    async for chunk in call_deepseek_stream(messages, temperature=0.4, max_tokens=2048):
        yield chunk