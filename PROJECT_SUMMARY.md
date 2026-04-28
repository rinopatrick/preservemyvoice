# PreserveMyVoice — Project Summary

## Mission
Open source voice banking for people at risk of losing their ability to speak (ALS, throat cancer, Parkinson's, MS, etc.).

## What Was Built

A full-stack, privacy-first voice banking platform with:

### Backend (Python/FastAPI)
- **FastAPI REST API** with 5 endpoints (health, recordings, voice models, TTS)
- **SQLite database** with SQLAlchemy ORM (3 tables: recordings, models, TTS history)
- **Audio processing** with librosa, soundfile, pydub
- **Voice cloning** integration with Coqui TTS (open source)
- **Local-first architecture** — all processing happens on user's machine by default
- **Pydantic settings** for configuration
- **Structured logging**

### Frontend (Vanilla JS PWA)
- **Progressive Web App** — works offline, installable
- **Real-time waveform visualization** during recording
- **Guided phrase recording** (10 curated phrases)
- **Voice model training** UI
- **Text-to-speech generation** with voice selection
- **Audio playback** for generated speech
- **Responsive design** — works on mobile and desktop
- **Animated particle background**

### Key Features
1. 🎤 Record voice samples via browser (WebRTC)
2. 🤖 Create personalized voice models
3. 💬 Generate speech in your own voice
4. 🔒 Privacy-first (local processing)
5. 📱 PWA (works offline)
6. 🗄️ Export/import voice models

## Project Structure
```
preservemyvoice/
├── src/preservemyvoice/
│   ├── __main__.py          # App entry point
│   ├── config.py            # Pydantic settings
│   ├── logging.py           # Structured logging
│   ├── exceptions.py        # Custom exception hierarchy
│   ├── domain/              # Database models
│   ├── services/            # Business logic
│   │   ├── audio_processor.py
│   │   ├── voice_cloner.py
│   │   └── __init__.py      # VoiceService orchestrator
│   ├── adapters/            # Infrastructure
│   │   └── __init__.py      # DB session, init
│   └── api/                 # REST API
│       ├── api.py           # FastAPI router
│       └── __init__.py
├── frontend/                # PWA frontend
│   ├── index.html           # Single-page app
│   └── dist/                # Built assets
├── tests/                   # pytest tests
├── Dockerfile               # Distroless container
└── pyproject.toml           # Dependencies
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/health` | Health check |
| POST | `/api/v1/recordings` | Upload voice recording |
| GET | `/api/v1/recordings` | List recordings |
| POST | `/api/v1/voice-models` | Train voice model |
| GET | `/api/v1/voice-models` | List voice models |
| POST | `/api/v1/tts` | Generate speech |

## Technology Stack

- **Python 3.13** — Modern Python
- **FastAPI** — High-performance web framework
- **SQLAlchemy** — ORM
- **Coqui TTS** — Open source voice cloning
- **Librosa** — Audio analysis
- **Pydantic** — Settings & validation
- **Vanilla JS** — Frontend (no frameworks)
- **SQLite** — Embedded database
- **Docker** — Containerization (distroless)

## Testing

5 unit tests, all passing:
- Settings configuration
- Voice service initialization
- Recording management
- Model management

```bash
uv run pytest tests/ -v
# 5 passed in 0.84s
```

## Running the Project

### Development
```bash
cd ~/projects/preservemyvoice
uv sync
uv run python -m preservemyvoice
```
Visit http://localhost:8000

### Docker
```bash
docker build -t preservemyvoice .
docker run -p 8000:8000 preservemyvoice
```

### API Test
```bash
curl http://localhost:8000/api/v1/health
# {"status":"healthy","app":"PreserveMyVoice"}
```

## Code Quality

- ✅ Type hints throughout
- ✅ Google-style docstrings
- ✅ Ruff linting & formatting
- ✅ Pytest with coverage
- ✅ Security-first (no hardcoded secrets)
- ✅ Distroless Docker (minimal attack surface)
- ✅ Non-root Docker user

## Impact

This project addresses a critical gap:
- Commercial voice banking: $500–$2,000
- PreserveMyVoice: **Free & open source**
- Accessible to anyone, anywhere
- Preserves identity, not just communication

For someone losing their voice to ALS or cancer, this isn't just technology — it's preserving a piece of who they are.

## Future Enhancements

- XTTS-v2 for better zero-shot cloning
- Fine-tuning support for production models
- Mobile apps (React Native/Flutter)
- Multi-language support
- Cloud sync (optional)
- Collaboration features for caregivers
- Voice donation system

## License

MIT — Free for anyone to use, modify, distribute.
