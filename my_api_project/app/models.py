from pydantic import BaseModel, Field

class TranslateRequest(BaseModel):
    text: str = Field(..., min_length=1, description="需要翻译的文本")
    target_lang: str = Field("en", description="目标语言代码")

class BattleRequest(BaseModel):
    attacker: str = Field(..., description="进攻方")
    defender: str = Field(..., description="防守方")
    location: str = Field(..., description="战场地点")
    plot: str = Field(..., min_length=10, description="战斗情节概要")
    style: str = Field("classical", description="风格：classical / epic / dark")