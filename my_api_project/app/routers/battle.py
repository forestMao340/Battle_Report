from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.models import BattleRequest
from app.services.battle import generate_battle_report,generate_battle_report_stream

router = APIRouter(prefix="/battle_report", tags=["战报"])

@router.post("/")
async def battle_report_endpoint(req: BattleRequest):
    report = await generate_battle_report(req)
    return {
        "attacker": req.attacker,
        "defender": req.defender,
        "location": req.location,
        "style": req.style,
        "report": report
    }

@router.post("/stream")
async def battle_report_stream_endpoint(req: BattleRequest):
    """
    流式战报生成，返回 text/event-stream，边生成边输出。
    """
    # 可以选择先做简单参数校验，然后直接返回 StreamingResponse
    return StreamingResponse(
        generate_battle_report_stream(req),
        media_type="text/event-stream"   # 也可用 "text/plain"
    )