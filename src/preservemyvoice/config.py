from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration."""

    APP_NAME: str = "PreserveMyVoice"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    DATABASE_URL: str = "sqlite:///./preservemyvoice.db"
    UPLOAD_DIR: str = "./uploads"
    MODELS_DIR: str = "./voice_models"
    MAX_RECORDING_SIZE: int = 50 * 1024 * 1024  # 50MB
    ALLOWED_AUDIO_FORMATS: list[str] = ["wav", "mp3", "flac", "m4a"]
    SAMPLE_RATE: int = 22050
    N_FFT: int = 2048
    HOP_LENGTH: int = 512
    N_MELS: int = 80

    # Guided phrases for voice recording
    GUIDED_PHRASES: list[str] = [
        "The quick brown fox jumps over the lazy dog.",
        "Hello, how are you today?",
        "I love you very much.",
        "Please pass the salt.",
        "What time is it?",
        "I would like a cup of tea.",
        "The weather is beautiful today.",
        "Can you help me with this?",
        "Thank you for everything.",
        "Good morning, have a nice day.",
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
