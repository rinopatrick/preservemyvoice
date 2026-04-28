import uuid
from pathlib import Path

import librosa
import numpy as np
import soundfile as sf
from pydub import AudioSegment

from ..config import settings
from ..exceptions import InvalidAudioError, StorageError


class AudioProcessor:
    """Handles audio file processing and validation."""

    def __init__(self):
        self.upload_dir = Path(settings.UPLOAD_DIR)
        self.models_dir = Path(settings.MODELS_DIR)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.models_dir.mkdir(parents=True, exist_ok=True)

    def save_uploaded_file(
        self, file_content: bytes, filename: str, user_id: str
    ) -> Path:
        """Save an uploaded audio file."""
        try:
            user_dir = self.upload_dir / user_id
            user_dir.mkdir(parents=True, exist_ok=True)

            file_ext = Path(filename).suffix.lower()
            safe_filename = f"{uuid.uuid4().hex}{file_ext}"
            filepath = user_dir / safe_filename

            with filepath.open("wb") as f:
                f.write(file_content)

            return filepath
        except Exception as e:
            raise StorageError(f"Failed to save file: {e}") from e

    def convert_to_wav(self, filepath: Path) -> Path:
        """Convert audio file to WAV format."""
        try:
            if filepath.suffix.lower() != ".wav":
                audio = AudioSegment.from_file(str(filepath))
                wav_path = filepath.with_suffix(".wav")
                audio.export(str(wav_path), format="wav")
                return wav_path
            return filepath
        except Exception as e:
            raise InvalidAudioError(f"Failed to convert audio: {e}")

    def validate_and_load_audio(self, filepath: Path) -> tuple[np.ndarray, int]:
        """Validate audio file and load it."""
        try:
            # Load with librosa
            y, sr = librosa.load(filepath, sr=settings.SAMPLE_RATE)

            # Check duration
            duration = len(y) / sr
            if duration < 1.0:
                raise InvalidAudioError("Audio too short (minimum 1 second)")
            if duration > 60.0:
                raise InvalidAudioError("Audio too long (maximum 60 seconds)")

            # Check for silence
            rms = np.sqrt(np.mean(y**2))
            if rms < 0.01:
                raise InvalidAudioError("Audio is too silent")

            return y, sr
        except InvalidAudioError:
            raise
        except Exception as e:
            raise InvalidAudioError(f"Invalid audio file: {e}") from e

    def extract_mfcc(self, y: np.ndarray, sr: int) -> np.ndarray:
        """Extract MFCC features from audio."""
        mfcc = librosa.feature.mfcc(
            y=y, sr=sr, n_mfcc=13, n_fft=settings.N_FFT, hop_length=settings.HOP_LENGTH
        )
        return mfcc.T

    def save_tts_output(
        self, audio_data: bytes, sample_rate: int, user_id: str, prefix: str = "tts"
    ) -> Path:
        """Save generated TTS audio."""
        try:
            user_dir = self.upload_dir / user_id
            user_dir.mkdir(parents=True, exist_ok=True)

            filename = f"{prefix}_{uuid.uuid4().hex[:8]}.wav"
            filepath = user_dir / filename

            sf.write(filepath, audio_data, sample_rate)
            return filepath
        except Exception as e:
            raise StorageError(f"Failed to save TTS output: {e}") from e

    def cleanup_file(self, filepath: Path) -> None:
        """Remove a file."""
        try:
            if filepath.exists():
                filepath.unlink()
        except Exception:
            pass
