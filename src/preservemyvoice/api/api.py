from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from ..adapters import get_db, init_db
from ..exceptions import (
    InvalidAudioError,
    ModelNotFoundError,
    StorageError,
    VoiceCloningError,
)
from ..services import VoiceService

router = APIRouter(prefix="/api/v1", tags=["voice"])


def get_voice_service(db: Session = Depends(get_db)) -> VoiceService:
    return VoiceService(db)


init_db()


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "app": "PreserveMyVoice"}


@router.post("/recordings")
async def upload_recording(
    user_id: str = Form(...),
    phrase_text: str | None = Form(None),
    file: UploadFile = File(...),
    voice_service: VoiceService = Depends(get_voice_service),
):
    """Upload a voice recording."""
    try:
        file_content = await file.read()
        recording = voice_service.create_recording(
            user_id=user_id,
            file_content=file_content,
            filename=file.filename or "recording.wav",
            phrase_text=phrase_text,
        )
        return {
            "id": recording.id,
            "user_id": recording.user_id,
            "filename": recording.filename,
            "duration": recording.duration,
            "sample_rate": recording.sample_rate,
            "phrase_text": recording.phrase_text,
            "created_at": recording.created_at.isoformat(),
        }
    except InvalidAudioError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )
    except StorageError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Recording upload failed: {e}",
        )


@router.get("/recordings", response_model=list[dict])
async def list_recordings(
    user_id: str,
    voice_service: VoiceService = Depends(get_voice_service),
):
    """List all recordings for a user."""
    recordings = voice_service.get_user_recordings(user_id)
    return [
        {
            "id": r.id,
            "filename": r.filename,
            "duration": r.duration,
            "sample_rate": r.sample_rate,
            "phrase_text": r.phrase_text,
            "is_valid": r.is_valid,
            "created_at": r.created_at.isoformat(),
        }
        for r in recordings
    ]


@router.post("/voice-models")
async def create_voice_model(
    user_id: str = Form(...),
    model_name: str = Form(...),
    recording_ids: str = Form(...),
    voice_service: VoiceService = Depends(get_voice_service),
):
    """Train a voice model from recordings."""
    try:
        import json

        ids = json.loads(recording_ids)
        model = voice_service.train_voice_model(
            user_id=user_id,
            recording_ids=ids,
            model_name=model_name,
        )
        return {
            "id": model.id,
            "user_id": model.user_id,
            "model_name": model.model_name,
            "training_status": model.training_status,
            "training_progress": model.training_progress,
            "num_recordings": model.num_recordings,
            "quality_score": model.quality_score,
            "created_at": model.created_at.isoformat(),
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except VoiceCloningError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Voice model training failed: {e}",
        )


@router.get("/voice-models", response_model=list[dict])
async def list_voice_models(
    user_id: str,
    voice_service: VoiceService = Depends(get_voice_service),
):
    """List all voice models for a user."""
    models = voice_service.get_user_models(user_id)
    return [
        {
            "id": m.id,
            "model_name": m.model_name,
            "training_status": m.training_status,
            "training_progress": m.training_progress,
            "num_recordings": m.num_recordings,
            "quality_score": m.quality_score,
            "created_at": m.created_at.isoformat(),
        }
        for m in models
    ]


@router.post("/tts")
async def generate_tts(
    user_id: str = Form(...),
    voice_model_id: int = Form(...),
    text: str = Form(...),
    language: str = Form("id"),
    voice_service: VoiceService = Depends(get_voice_service),
):
    """Generate speech from text."""
    try:
        tts = voice_service.generate_speech(
            user_id=user_id,
            voice_model_id=voice_model_id,
            text=text,
        )
        return {
            "id": tts.id,
            "voice_model_id": tts.voice_model_id,
            "input_text": tts.input_text,
            "output_filename": tts.output_filename,
            "output_path": tts.output_path,
            "duration": tts.duration,
            "created_at": tts.created_at.isoformat(),
        }
    except ModelNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"TTS generation failed: {e}",
        )
