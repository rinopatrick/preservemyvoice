from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

from ..domain import TTSGeneration, VoiceModel, VoiceRecording
from ..exceptions import ModelNotFoundError

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


class VoiceService:
    """Orchestrates voice recording, cloning, and TTS generation."""

    def __init__(self, db: "Session") -> None:
        self.db = db
        # Lazy imports to avoid circular dependencies
        from .audio_processor import AudioProcessor
        from .voice_cloner import VoiceCloner

        self.audio_processor = AudioProcessor()
        self.voice_cloner = VoiceCloner()

    def create_recording(
        self,
        user_id: str,
        file_content: bytes,
        filename: str,
        phrase_text: str | None = None,
    ) -> VoiceRecording:
        """Save and process a new voice recording."""
        filepath = self.audio_processor.save_uploaded_file(
            file_content, filename, user_id
        )

        try:
            wav_path = self.audio_processor.convert_to_wav(filepath)
            y, sr = self.audio_processor.validate_and_load_audio(wav_path)
            duration = len(y) / sr

            recording = VoiceRecording(
                user_id=user_id,
                filename=filename,
                filepath=str(wav_path),
                duration=duration,
                sample_rate=sr,
                phrase_text=phrase_text,
                is_valid=True,
            )
            self.db.add(recording)
            self.db.commit()
            self.db.refresh(recording)
            self.audio_processor.cleanup_file(filepath)
            return recording
        except Exception as e:
            self.audio_processor.cleanup_file(filepath)
            raise e

    def train_voice_model(
        self, user_id: str, recording_ids: list[int], model_name: str
    ) -> VoiceModel:
        """Train a voice model from recordings."""
        recordings = (
            self.db.query(VoiceRecording)
            .filter(
                VoiceRecording.id.in_(recording_ids),
                VoiceRecording.user_id == user_id,
                VoiceRecording.is_valid,
            )
            .all()
        )

        if not recordings:
            raise ValueError("No valid recordings found")

        model = VoiceModel(
            user_id=user_id,
            model_name=model_name,
            model_path="",
            training_status="training",
            training_progress=0.0,
            num_recordings=len(recordings),
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)

        try:
            audio_files = [Path(r.filepath) for r in recordings]
            model_dir = self.audio_processor.models_dir / str(model.id)
            result = self.voice_cloner.clone_voice(audio_files, model_dir, model_name)

            model.model_path = result["metadata_path"]
            model.training_status = "completed"
            model.training_progress = 1.0
            model.quality_score = 0.9
            model.updated_at = datetime.utcnow()

            self.db.commit()
            self.db.refresh(model)
            return model
        except Exception as e:
            model.training_status = "failed"
            self.db.commit()
            raise e

    def generate_speech(
        self,
        user_id: str,
        voice_model_id: int,
        text: str,
    ) -> TTSGeneration:
        """Generate speech from text using a voice model."""
        model = (
            self.db.query(VoiceModel)
            .filter(
                VoiceModel.id == voice_model_id,
                VoiceModel.user_id == user_id,
            )
            .first()
        )

        if not model:
            raise ModelNotFoundError("Voice model not found")
        if model.training_status != "completed":
            raise ValueError("Voice model not ready")

        try:
            output_path = self.audio_processor.save_tts_output(
                b"", 22050, user_id, prefix=f"tts_{model.id}"
            )

            voice_samples = [
                Path(r.filepath)
                for r in self.db.query(VoiceRecording)
                .filter(
                    VoiceRecording.user_id == user_id,
                    VoiceRecording.is_valid,
                )
                .limit(3)
                .all()
            ]

            if voice_samples:
                output_path = self.voice_cloner.synthesize(
                    text, output_path, voice_samples=voice_samples
                )

            duration = None
            try:
                import librosa

                y, sr = librosa.load(output_path)
                duration = len(y) / sr
            except Exception:
                pass

            tts = TTSGeneration(
                user_id=user_id,
                voice_model_id=voice_model_id,
                input_text=text,
                output_filename=output_path.name,
                output_path=str(output_path),
                duration=duration,
            )
            self.db.add(tts)
            self.db.commit()
            self.db.refresh(tts)
            return tts
        except Exception as e:
            raise e

    def get_user_recordings(self, user_id: str) -> list[VoiceRecording]:
        """Get all recordings for a user."""
        return (
            self.db.query(VoiceRecording)
            .filter(VoiceRecording.user_id == user_id)
            .order_by(VoiceRecording.created_at.desc())
            .all()
        )

    def get_user_models(self, user_id: str) -> list[VoiceModel]:
        """Get all voice models for a user."""
        return (
            self.db.query(VoiceModel)
            .filter(VoiceModel.user_id == user_id)
            .order_by(VoiceModel.created_at.desc())
            .all()
        )
