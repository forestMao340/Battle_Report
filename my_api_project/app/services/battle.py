import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
from fastapi import HTTPException
from app.services.ai_client import call_deepseek, call_deepseek_stream
from app.models import BattleRequest
import chromadb
from chromadb.utils import embedding_functions

# ---------- 初始化 ChromaDB ----------
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="paraphrase-multilingual-MiniLM-L12-v2"
)
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("battle_knowledge")

def retrieve_context(query: str, top_k: int = 3) -> str:
    """根据查询检索相关背景资料"""
    try:
        results = collection.query(query_texts=[query], n_results=top_k)
        if results['documents'] and results['documents'][0]:
            return "\n\n---\n\n".join(results['documents'][0])
        return ""
    except Exception as e:
        print(f"⚠️ 检索失败：{e}")
        return ""

# ---------- 公共函数：构造消息 ----------
def build_battle_messages(req: BattleRequest, context: str):
    style_prompts = {
        "classical": ("你是一位天庭说书人，擅长用《西游记》风格的古典白话讲述神魔大战。", "古典白话"),
        "epic": ("你是一位北欧女武神瓦尔基里，以史诗般的庄严口吻记录诸神黄昏之战。", "庄严史诗"),
        "dark": ("你是一位帝国记录官，以哥特式黑暗风格书写战争。", "黑暗哥特")
    }
    if req.style not in style_prompts:
        raise HTTPException(status_code=400, detail=f"不支持的风格: {req.style}")

    system_prompt, style_name = style_prompts[req.style]
    if context:
        system_prompt += f"\n\n请参考以下背景资料进行创作：\n{context}"
    else:
        system_prompt += "\n\n（无相关背景资料，请凭你的知识创作。）"

    user_prompt = f"战斗双方：{req.attacker} vs {req.defender}\n地点：{req.location}\n情节概要：{req.plot}\n风格：{style_name}\n战报需包含标题、战斗过程、高潮部分和结尾，约400-600字。"

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

# ---------- 非流式战报 ----------
async def generate_battle_report(req: BattleRequest) -> str:
    query = f"{req.attacker} {req.defender} {req.location} {req.style} {req.plot}"
    context = retrieve_context(query, top_k=3)
    messages = build_battle_messages(req, context)
    return await call_deepseek(messages, temperature=0.7, max_tokens=2048)

# ---------- 流式战报 ----------
async def generate_battle_report_stream(req: BattleRequest):
    query = f"{req.attacker} {req.defender} {req.location} {req.style} {req.plot}"
    context = retrieve_context(query, top_k=3)
    messages = build_battle_messages(req, context)
    # 使用流式调用
    async for chunk in call_deepseek_stream(messages, temperature=0.7, max_tokens=2048):
        yield chunk