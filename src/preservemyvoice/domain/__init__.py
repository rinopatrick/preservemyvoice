from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class VoiceRecording(Base):
    """Stores voice recordings for a user."""

    __tablename__ = "voice_recordings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False)
    filename = Column(String, nullable=False)
    filepath = Column(String, nullable=False)
    duration = Column(Float, nullable=False)  # seconds
    sample_rate = Column(Integer, nullable=False)
    phrase_text = Column(Text, nullable=True)
    is_valid = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class VoiceModel(Base):
    """Stores trained voice models."""

    __tablename__ = "voice_models"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False)
    model_name = Column(String, nullable=False)
    model_path = Column(String, nullable=False)
    training_status = Column(
        String, default="pending"
    )  # pending, training, completed, failed
    training_progress = Column(Float, default=0.0)  # 0.0 to 1.0
    num_recordings = Column(Integer, default=0)
    quality_score = Column(Float, nullable=True)  # 0.0 to 1.0
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class TTSGeneration(Base):
    """Stores TTS generation history."""

    __tablename__ = "tts_generations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False)
    voice_model_id = Column(Integer, nullable=False)
    input_text = Column(Text, nullable=False)
    output_filename = Column(String, nullable=False)
    output_path = Column(String, nullable=False)
    duration = Column(Float, nullable=True)  # seconds
    created_at = Column(DateTime, default=datetime.utcnow)
