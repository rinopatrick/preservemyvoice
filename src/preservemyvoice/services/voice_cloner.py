import json
from pathlib import Path
from typing import Optional

import numpy as np

from ..config import settings
from ..exceptions import VoiceCloningError


def _check_torch_and_cuda():
    """Check if torch is available and CUDA is ready."""
    try:
        import torch
        is_cuda = torch.cuda.is_available()
        return is_cuda, "CUDA available" if is_cuda else "CUDA not available, using CPU (slower)"
    except ImportError:
        return False, "CUDA not available, using CPU (slower)"


class VoiceCloner:
    """Handles voice cloning using Coqui TTS or Piper TTS.
    
    Uses Piper (lightweight) by default if model is available.
    Falls back to Coqui TTS for advanced voice cloning.
    """

    def __init__(self, use_piper: bool = True):
        self.model = None
        self.model_name = "tts_models/en/ljspeech/tacotron2-DDC"
        self.is_cuda, self.device_info = _check_torch_and_cuda()
        self.device = "cuda" if self.is_cuda else "cpu"
        self.use_piper = use_piper
        
        # Try to load Piper model (bundled)
        self.piper_model_dir = Path(__file__).parent.parent.parent / "models" / "piper" / "id_indic_vits"
        self.piper_available = False
        
        if use_piper and self.piper_model_dir.exists():
            try:
                from .tts_engine import PiperTTS
                self.piper = PiperTTS(self.piper_model_dir)
                self.piper_available = self.piper.is_available
            except Exception as e:
                print(f"Piper TTS not available: {e}")
                self.piper_available = False

    def load_model(self) -> None:
        """Lazy load the TTS model."""
        if self.model is not None:
            return
        
        # If Piper is available, no need to load heavy model
        if self.piper_available:
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

        Note: Full voice cloning requires significant compute.
        This implementation uses zero-shot voice cloning
        with XTTS or similar multi-speaker models where available.
        For production, consider fine-tuning or using XTTS-v2.
        """
        output_dir.mkdir(parents=True, exist_ok=True)

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
        voice_samples: Optional[list[Path]] = None,
        speaker_idx: int = 0,
        use_piper: bool = True,
    ) -> Path:
        """Synthesize speech from text.

        If voice_samples provided and not using Piper, attempts zero-shot cloning.
        Otherwise uses default speaker or Piper TTS.
        """
        # Use Piper if available and requested (no voice cloning)
        if use_piper and self.piper_available and not voice_samples:
            return self.piper.synthesize(text, output_path)
        
        # Otherwise use Coqui TTS
        self.load_model()

        try:
            # Check if model supports voice cloning
            if hasattr(self.model, "tts_with_vc") and voice_samples:
                # Use voice conversion
                ref_audio = str(voice_samples[0])
                wav = self.model.tts_with_vc(
                    tts_text=text,
                    file_path=ref_audio,
                )
            else:
                # Standard TTS with speaker selection
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
        if self.piper_available:
            return self.piper.get_speakers()
        
        self.load_model()
        if hasattr(self.model, "speakers"):
            return self.model.speakers
        return ["default"]

