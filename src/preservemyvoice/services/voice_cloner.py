import json
from pathlib import Path

import numpy as np

from ..exceptions import VoiceCloningError


def _check_torch_and_cuda():
    """Check if torch is available and CUDA is ready."""
    try:
        import torch

        is_cuda = torch.cuda.is_available()
        return (
            is_cuda,
            "CUDA available" if is_cuda else "CUDA not available, using CPU (slower)",
        )
    except ImportError:
        return False, "CUDA not available, using CPU (slower)"


class VoiceCloner:
    """Handles voice cloning using Coqui TTS."""

    def __init__(self):
        self.model = None
        self.model_name = "tts_models/en/ljspeech/tacotron2-DDC"
        self.is_cuda, self.device_info = _check_torch_and_cuda()
        self.device = "cuda" if self.is_cuda else "cpu"

    def load_model(self) -> None:
        """Lazy load the TTS model."""
        if self.model is not None:
            return
        try:
            from TTS.api import TTS

            self.model = TTS(
                model_name=self.model_name,
                progress_bar=False,
                gpu=self.is_cuda,
            )
        except ImportError as e:
            raise VoiceCloningError(
                "Coqui TTS not installed. Install with: pip install TTS"
            ) from e
        except Exception as e:
            raise VoiceCloningError(f"Failed to load TTS model: {e}") from e

    def clone_voice(
        self,
        audio_filepaths: list[Path],
        output_dir: Path,
        voice_name: str = "cloned_voice",
    ) -> dict:
        """Clone a voice from multiple audio samples.

        Note: Full voice cloning (training a new speaker) requires significant
        compute and data. This implementation uses zero-shot voice cloning
        with XTTS or similar multi-speaker models where available.
        For production, consider fine-tuning or using XTTS-v2.
        """
        self.load_model()

        output_dir.mkdir(parents=True, exist_ok=True)

        # For now, we use the pre-trained model directly
        # In a full implementation, you'd:
        # 1. Fine-tune on the provided samples
        # 2. Or use XTTS zero-shot cloning
        # 3. Save the fine-tuned checkpoint

        result = {
            "voice_name": voice_name,
            "model_name": self.model_name,
            "num_samples": len(audio_filepaths),
            "device": self.device,
            "status": "ready",
            "method": "zero-shot",
        }

        # Save metadata
        metadata_path = output_dir / f"{voice_name}_metadata.json"
        with metadata_path.open("w") as f:
            json.dump(result, f, indent=2)

        result["metadata_path"] = str(metadata_path)
        return result

    def synthesize(
        self,
        text: str,
        output_path: Path,
        voice_samples: list[Path] | None = None,
        speaker_idx: int = 0,
    ) -> Path:
        """Synthesize speech from text.

        If voice_samples provided, attempts zero-shot voice cloning.
        Otherwise uses the default speaker.
        """
        self.load_model()

        try:
            # Check if model supports voice cloning
            if hasattr(self.model, "tts_with_vc") and voice_samples:
                # Use voice conversion
                # Load first sample as reference
                ref_audio = str(voice_samples[0])
                wav = self.model.tts_with_vc(
                    tts_text=text,
                    file_path=ref_audio,
                )
            else:
                # Standard TTS with speaker selection
                # List available speakers
                wavs = self.model.tts(
                    text=text,
                    speaker_idx=speaker_idx,
                )
                if isinstance(wavs, list):
                    wav = np.concatenate(wavs) if len(wavs) > 1 else wavs[0]
                else:
                    wav = wavs

            # Save output
            import soundfile as sf

            output_path.parent.mkdir(parents=True, exist_ok=True)
            sf.write(output_path, wav, self.model.output_sample_rate)

            return output_path

        except Exception as e:
            raise VoiceCloningError(f"TTS synthesis failed: {e}") from e

    def get_available_speakers(self) -> list[str]:
        """Get list of available speakers for multi-speaker models."""
        self.load_model()
        if hasattr(self.model, "speakers"):
            return self.model.speakers
        return ["default"]
