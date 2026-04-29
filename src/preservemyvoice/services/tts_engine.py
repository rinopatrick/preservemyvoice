import subprocess
import numpy as np
from pathlib import Path
from typing import Optional, List
import logging
import json

logger = logging.getLogger(__name__)


class PiperTTS:
    """High-quality offline TTS using Piper.
    
    Uses bundled models for Indonesian and English.
    No internet required after setup.
    """
    
    def __init__(self, models_dir: Path):
        self.models_dir = models_dir
        self.piper_bin = models_dir.parent / "piper" / "piper"
        self.espeak_bin = models_dir.parent / "piper" / "espeak-ng"
        
        # Available models
        self.models = {
            'id': self.models_dir / "id_ID-news_tts-medium.onnx",
            'en': self.models_dir / "en_US-ljspeech-high.onnx",
        }
        
        # Model configs
        self.configs = {}
        for lang, model_path in self.models.items():
            config_path = str(model_path) + ".json"
            if Path(config_path).exists():
                with open(config_path) as f:
                    self.configs[lang] = json.load(f)
        
        # Check availability
        self.is_available = self._check_availability()
    
    def _check_availability(self) -> bool:
        """Check if Piper and models are available."""
        if not self.piper_bin.exists():
            logger.warning(f"Piper binary not found: {self.piper_bin}")
            return False
        
        if not self.espeak_bin.exists():
            logger.warning(f"espeak-ng not found: {self.espeak_bin}")
            return False
        
        for lang, model_path in self.models.items():
            if not model_path.exists():
                logger.warning(f"Model not found for {lang}: {model_path}")
                return False
        
        # Test run
        try:
            result = subprocess.run(
                [str(self.piper_bin), "--help"],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception as e:
            logger.warning(f"Piper test failed: {e}")
            return False
    
    def synthesize(
        self,
        text: str,
        output_path: Path,
        language: str = "id",
        speaker: Optional[str] = None
    ) -> Path:
        """Convert text to speech using Piper.
        
        Args:
            text: Text to synthesize
            output_path: Where to save WAV file
            language: Language code (id, en)
            speaker: Speaker name (if multi-speaker model)
        
        Returns:
            Path to generated audio file
        """
        if not self.is_available:
            raise RuntimeError("Piper TTS engine not available")
        
        model_path = self.models.get(language)
        if not model_path or not model_path.exists():
            raise ValueError(f"No model available for language: {language}")
        
        # Create output directory
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Build Piper command
        cmd = [
            str(self.piper_bin),
            "-m", str(model_path),
            "-f", str(output_path),
        ]
        
        # Add speaker if specified
        if speaker:
            cmd.extend(["-s", speaker])
        
        # Run Piper with text from stdin
        try:
            result = subprocess.run(
                cmd,
                input=text.encode('utf-8'),
                capture_output=True,
                timeout=30
            )
            
            if result.returncode != 0:
                error_msg = result.stderr.decode('utf-8', errors='ignore')
                raise RuntimeError(f"Piper failed: {error_msg}")
            
            if not output_path.exists():
                raise RuntimeError("Piper did not generate output file")
            
            logger.info(f"Generated audio: {output_path} ({output_path.stat().st_size} bytes)")
            return output_path
            
        except subprocess.TimeoutExpired:
            raise RuntimeError("Piper synthesis timed out")
        except Exception as e:
            raise RuntimeError(f"Piper synthesis failed: {e}")
    
    def get_speakers(self, language: str = "id") -> List[str]:
        """Get available speakers for a language."""
        config = self.configs.get(language, {})
        speakers = config.get("speakers", [])
        return speakers if speakers else ["default"]
    
    def get_languages(self) -> List[str]:
        """Get list of available languages."""
        return [lang for lang, path in self.models.items() if path.exists()]


class TTSManager:
    """Manages TTS engines with fallback support."""
    
    def __init__(self, models_dir: Path):
        self.models_dir = models_dir
        self.piper = PiperTTS(models_dir)
        self.coqui = None
        
        # Try to load Coqui as fallback
        try:
            from .voice_cloner import VoiceCloner
            self.coqui = VoiceCloner(use_piper=False)
            logger.info("Coqui TTS loaded as fallback")
        except Exception as e:
            logger.debug(f"Coqui TTS not available: {e}")
    
    def synthesize(
        self,
        text: str,
        output_path: Path,
        language: str = "id",
        use_piper: bool = True,
        voice_samples: Optional[List[Path]] = None
    ) -> Path:
        """Synthesize speech with automatic engine selection.
        
        Priority:
        1. Voice cloning (Coqui) if voice_samples provided
        2. Piper if available and use_piper=True
        3. Coqui as fallback
        """
        # Voice cloning takes priority
        if voice_samples and self.coqui:
            logger.info("Using Coqui TTS for voice cloning")
            return self.coqui.synthesize(text, output_path, voice_samples)
        
        # Use Piper if available
        if use_piper and self.piper.is_available:
            logger.info(f"Using Piper TTS for {language}")
            return self.piper.synthesize(text, output_path, language)
        
        # Fallback to Coqui
        if self.coqui:
            logger.info("Using Coqui TTS as fallback")
            return self.coqui.synthesize(text, output_path)
        
        raise RuntimeError("No TTS engine available")
    
    def get_voices(self, language: str = "id") -> List[str]:
        """Get available voices/speakers."""
        return self.piper.get_speakers(language)
    
    def get_languages(self) -> List[str]:
        """Get available languages."""
        return self.piper.get_languages()
