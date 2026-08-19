from openai import AsyncOpenAI, APIError, APIConnectionError, RateLimitError, AuthenticationError
from fastapi import HTTPException
from app.config import settings
import os

client = AsyncOpenAI(api_key=settings.DEEPSEEK_API_KEY, base_url=settings.BASE_URL)

async def call_deepseek(messages, temperature=0.7, max_tokens=1024):
    try:
        response = await client.chat.completions.create(
            model=settings.MODEL,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=False
        )
        return response.choices[0].message.content.strip()
    except AuthenticationError:
        raise HTTPException(status_code=401, detail="API 密钥无效")
    except RateLimitError:
        raise HTTPException(status_code=429, detail="请求频率超限")
    except APIConnectionError:
        raise HTTPException(status_code=503, detail="AI 服务连接失败")
    except APIError as e:
        if "model" in str(e).lower():
            raise HTTPException(status_code=400, detail=f"模型不支持: {str(e)}")
        raise HTTPException(status_code=500, detail=f"API 调用失败: {str(e)}")
    except Exception as e:
        # 将异常信息转为 ASCII 安全的字符串（替换非 ASCII 字符）
        safe_msg = str(e).encode('ascii', errors='replace').decode('ascii')
        raise HTTPException(status_code=500, detail=f"服务内部错误: {safe_msg}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务内部错误: {str(e)}")

async def call_deepseek_stream(messages, temperature=0.7, max_tokens=2048):
    """
    异步生成器，逐块产出 AI 回复的文本片段。
    """
    try:
        stream = await client.chat.completions.create(
            model=settings.MODEL,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True
        )
        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    except Exception as e:
        # 将错误信息作为块输出（这样客户端也能收到错误提示）
        yield f"\n[错误] {str(e)}"