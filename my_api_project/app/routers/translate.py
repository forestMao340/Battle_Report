from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import StreamingResponse
from app.models import TranslateRequest
from app.services.translate import translate_text, translate_classical, translate_text_stream,translate_classical_stream
from app.utils.helpers import detect_source_lang

router = APIRouter(prefix="/translate", tags=["翻译"])

@router.get("/")
async def translate_get(text: str = Query(..., min_length=1), target_lang: str = "en"):
    if not text.strip():
        raise HTTPException(400, "text不能为空")
    translated = await translate_text(text, target_lang)
    return {
        "original": text,
        "source_lang": detect_source_lang(text),
        "target_lang": target_lang,
        "translated": translated
    }

@router.post("/")
async def translate_post(request: TranslateRequest):
    if not request.text.strip():
        raise HTTPException(400, "text不能为空")
    translated = await translate_text(request.text, request.target_lang)
    return {
        "original": request.text,
        "source_lang": detect_source_lang(request.text),
        "target_lang": request.target_lang,
        "translated": translated
    }

@router.post("/stream")
async def translate_stream(request: TranslateRequest):
    """
    流式翻译接口：返回 text/event-stream，逐块输出翻译内容。
    """
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="text不能为空")
    
    # 返回 StreamingResponse，media_type 可选 text/plain 或 text/event-stream
    return StreamingResponse(
        translate_text_stream(request.text, request.target_lang),
        media_type="text/event-stream"   # 或 "text/plain"
    )

@router.post("/classical")
async def translate_classical_endpoint(request: TranslateRequest):
    if not request.text.strip():
        raise HTTPException(400, "text不能为空")
    translated = await translate_classical(request.text)
    return {
        "original": request.text,
        "source_lang": "classical_chinese",
        "target_lang": "modern_chinese",
        "translated": translated
    }

@router.post("/classical/stream")
async def translate_classical_stream_endpoint(request: TranslateRequest):
    """
    流式文言文→白话文翻译，返回 text/event-stream。
    """
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="text不能为空")
    
    return StreamingResponse(
        translate_classical_stream(request.text),
        media_type="text/event-stream"
    )
