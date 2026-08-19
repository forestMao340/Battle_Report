from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.routers import translate, battle

app = FastAPI(title="AI 多功能 API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],           # 允许所有 HTTP 方法
    allow_headers=["*"],           # 允许所有请求头
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(translate.router)
app.include_router(battle.router)

@app.get("/")
async def root():
    return {
        "message": "欢迎使用 AI 多功能 API",
        "docs": "/docs"
    }