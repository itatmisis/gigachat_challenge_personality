import multiprocessing as mp

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    uvicorn_host: str = "localhost"
    uvicorn_port: int = 8000
    uvicorn_workers: int = mp.cpu_count() * 2
    uvicorn_log_level: str = "WARNING"

    redis_host: str = "localhost"
    redis_port: int = 6379

    kandinsky_api_key: str
    kandinsky_api_secret: str
    gigachat_credentials: str
    tg_bot_token: str
    photoroom_api_key: str
    base_path: str = "https://kodiki-hack.ru:8000"

    remove_bg: bool = False

    model_config = SettingsConfigDict(env_prefix="_", env_file=".env")


app_settings = AppSettings()
