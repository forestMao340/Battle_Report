import os

class Settings:
    DEEPSEEK_API_KEY: str = os.environ.get("DEEPSEEK_API_KEY", "")
    BASE_URL: str = "https://api.deepseek.com"
    MODEL: str = "deepseek-v4-flash"

settings = Settings()