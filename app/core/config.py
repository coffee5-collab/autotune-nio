from __future__ import annotations

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "AutoTune NIO"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    SAMPLE_RATE: int = 48000
    FFT_SIZE: int = 8192
    HOP_LENGTH: int = 2048

    EQ_FILTER_COUNT: int = 7
    EQ_GAIN_MIN: float = -10.0
    EQ_GAIN_MAX: float = 10.0
    EQ_Q_MIN: float = 0.5
    EQ_Q_MAX: float = 10.0

    class Config:
        env_file = ".env"


settings = Settings()
