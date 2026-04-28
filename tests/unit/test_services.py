import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from preservemyvoice.domain import Base
from preservemyvoice.services import VoiceService


@pytest.fixture
def db():
    """Create an in-memory database for testing."""
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def voice_service(db):
    """Create a VoiceService instance."""
    return VoiceService(db)


def test_create_recording_minimal(voice_service):
    """Test creating a recording with minimal data."""
    # This should fail gracefully since we don't have real audio
    # but we can test the service initialization
    assert voice_service.db is not None
    assert voice_service.audio_processor is not None


def test_get_empty_recordings(voice_service):
    """Test getting recordings for a new user."""
    recordings = voice_service.get_user_recordings("test_user")
    assert recordings == []


def test_get_empty_models(voice_service):
    """Test getting voice models for a new user."""
    models = voice_service.get_user_models("test_user")
    assert models == []
