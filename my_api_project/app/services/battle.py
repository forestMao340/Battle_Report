from fastapi import HTTPException
from app.services.ai_client import call_deepseek
from app.models import BattleRequest
from app.services.ai_client import call_deepseek_stream

async def generate_battle_report(req: BattleRequest) -> str:
    style_prompts = {
        "classical": ("你是一位说书人，擅长写神魔大战的古典白话战报。", "古典白话风格"),
        "epic": ("你是一位女武神，以史诗风格记录战争。", "庄严史诗风格"),
        "dark": ("你是一位帝国记录官，以黑暗哥特风格书写战争。", "黑暗哥特风格")
    }
    if req.style not in style_prompts:
        raise HTTPException(status_code=400, detail=f"不支持的风格: {req.style}")
    system_prompt, style_name = style_prompts[req.style]
    user_prompt = f"请为以下战斗写一份战报（{style_name}）：\n进攻方：{req.attacker}\n防守方：{req.defender}\n地点：{req.location}\n情节概要：{req.plot}\n要求：战报不少于300字，包含战斗过程、高潮和结尾。"
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    return await call_deepseek(messages, temperature=0.7, max_tokens=10240)

async def generate_battle_report_stream(req: BattleRequest):
    """
    异步生成器，流式返回战报内容。
    提示词与非流式版本保持一致，但使用流式 API 调用。
    """
    style_prompts = {
        "classical": (
            "你是一位天庭说书人，擅长用《西游记》风格的古典白话讲述神魔大战。语言要生动、豪迈，多用'话说''但见''好不'等章回体用语。",
            "请用古典白话风格撰写一份战报，描述这场大战的经过。"
        ),
        "epic": (
            "你是一位北欧女武神瓦尔基里，以史诗般的庄严口吻记录诸神黄昏之战。语言悲壮、肃穆，充满宿命感。",
            "请用北欧史诗风格撰写一份战报，描述这场末日般的决战。"
        ),
        "dark": (
            "你是一位帝国记录官，以哥特式黑暗风格书写战争。语言沉重、黑暗，充满死亡与混沌的意象。",
            "请用战锤40K哥特风格撰写一份战报，描绘这场血腥的战争。"
        )
    }
    if req.style not in style_prompts:
        yield f"错误：不支持的风格 '{req.style}'"
        return

    system_prompt, style_task = style_prompts[req.style]
    user_prompt = f"""
战斗双方：{req.attacker} vs {req.defender}
战场：{req.location}
情节概要：{req.plot}

{style_task}
战报需包含标题、战斗过程、高潮部分和结尾（如诗句或格言）。篇幅约400-600字。
"""
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    # 调用流式 API，逐块 yield 内容
    async for chunk in call_deepseek_stream(messages, temperature=0.7, max_tokens=10240):
        yield chunk
