"""Custom exception hierarchy for PreserveMyVoice."""


class AppError(Exception):
    """Base exception for all application errors."""


class VoiceRecordingError(AppError):
    """Raised when voice recording fails."""


class VoiceCloningError(AppError):
    """Raised when voice cloning fails."""


class ModelNotFoundError(AppError):
    """Raised when a voice model is not found."""


class InvalidAudioError(AppError):
    """Raised when audio file is invalid or corrupted."""


class StorageError(AppError):
    """Raised when file storage operations fail."""
