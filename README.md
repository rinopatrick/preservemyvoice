# PreserveMyVoice

> **Open source voice banking for people at risk of losing their ability to speak.**
> **100% Local AI — Zero Cloud Dependency**

## 🎯 The Problem

50,000+ people per year are diagnosed with conditions that will rob them of speech:
- **ALS (Lou Gehrig's disease)**
- **Throat cancer**
- **Parkinson's disease**
- **Multiple Sclerosis (MS)**
- **Stroke & neurological disorders**

Commercial voice banking costs **$500–$2,000**. In developing countries, most people have **zero options**. Once their voice is gone, they're given a generic robotic voice — stripping away a core piece of their identity.

## 💡 The Solution

**PreserveMyVoice** is a **100% local, open source voice banking platform** that:

✅ **Records** your voice via browser (WebRTC)  
✅ **Clones** your voice using neural AI (Coqui TTS)  
✅ **Generates** speech in YOUR voice from text  
✅ **Runs offline** — no internet required after setup  
✅ **Free forever** — no subscriptions, no cloud fees  
✅ **Private by design** — your voice never leaves your machine  

## 🔒 Why Local AI Matters

| Feature | PreserveMyVoice | Commercial Services |
|---------|----------------|--------------------|
| **Where AI runs** | 🖥️ Your computer | ☁️ Their servers |
| **Internet required** | ❌ After initial setup | ✅ Always |
| **Voice data shared** | ❌ Never | ✅ Yes (they store it) |
| **Works offline** | ✅ Yes | ❌ No |
| **Cost** | 💵 Free | 💰 $500–$2,000+ |
| **Medical privacy** | ✅ HIPAA-ready | ❌ Questionable |
| **Open source** | ✅ Auditable | ❌ Black box |

**Your voice is biometric data.** It's as personal as a fingerprint. Why upload it to a corporation's cloud when you can keep it on your own machine?

## 🤖 The AI Technology

### Neural Voice Cloning (Coqui TTS)

We use **Coqui TTS** — state-of-the-art open source neural TTS:

- **Tacotron 2** — Deep neural network for speech synthesis
- **WaveRNN/vocoder** — High-fidelity audio generation
- **Zero-shot voice cloning** — Clone voices from 3-5 samples
- **Multi-speaker models** — Switch between different voices

### How It Works

```
1. You record 5-10 guided phrases (50 seconds total)
   ↓
2. Audio processed locally with librosa (audio analysis)
   ↓
3. Coqui TTS trains a voice model on your samples
   ↓
4. Model saved locally (500MB–1GB)
   ↓
5. Type text → AI generates speech in YOUR voice
   ↓
6. Audio output saved/played — 100% offline
```

**No API calls. No cloud compute. No data exfiltration.**

## 🚀 Quick Start

### Prerequisites

- **Python 3.13** (or Docker)
- **5–10 minutes** for first-time setup
- **5–10 GB storage** (for AI models)
- **Optional**: NVIDIA GPU with CUDA (5–10x faster)

### Installation

#### Option 1: Native (Recommended)

```bash
# Clone or navigate to project
cd ~/projects/preservemyvoice

# Install dependencies
uv sync

# Run the application
uv run python -m preservemyvoice
```

Visit **http://localhost:8000**

#### Option 2: Docker

```bash
# Build
docker build -t preservemyvoice .

# Run
docker run -p 8000:8000 preservemyvoice
```

Visit **http://localhost:8000**

### First-Time Use

1. **Open browser** to http://localhost:8000
2. **Allow microphone access** when prompted
3. **Click "Next Phrase"** to get a guided sentence
4. **Click the red record button** ⏺ to record
5. **Repeat** for 5–10 phrases (more = better quality)
6. **Click "Upload All Recordings"**
7. **Name your voice model** and click "Create Voice Model"
8. **Wait 1–5 minutes** for AI training (faster with GPU)
9. **Type text** in the TTS box and click "Generate Speech"
10. **Hear yourself speak** — even after you've lost your voice

## 📖 Usage Guide

### Recording Your Voice

**Best practices:**
- Use a **quiet room** (no background noise)
- Speak **naturally** (like normal conversation)
- Keep **6–12 inches** from microphone
- Don't whisper or shout
- Read each phrase **once** clearly

**Guided phrases include:**
- "The quick brown fox jumps over the lazy dog."
- "Hello, how are you today?"
- "I love you very much."
- "Please pass the salt."
- "What time is it?"
- And 5 more...

### Creating a Voice Model

- **Minimum**: 5 recordings (30 seconds)
- **Good**: 8 recordings (1 minute)
- **Best**: 10 recordings (2 minutes)

More recordings = more natural-sounding voice.

### Generating Speech

1. Select your trained voice model from the dropdown
2. Type what you want to say (any length)
3. Click "Generate Speech"
4. Listen and download

**Typical generation speed:**
- **CPU**: 2–5x real-time (2 min audio = 30–60 sec generation)
- **GPU**: 0.2–0.5x real-time (2 min audio = 10–15 sec generation)

## 🏗️ Architecture

```
Frontend (PWA)                              Backend (FastAPI)
     │                                              │
     ├─ Record audio (WebRTC) ────────────────────▶│
     │                                              ├─ AudioProcessor
     │                                              │  (librosa, pydub)
     │                                              │
     ├─ Upload samples ────────────────────────────▶│
     │                                              ├─ VoiceCloner
     │                                              │  (Coqui TTS)
     │                                              │
     ◀─ Generate TTS ──────────────────────────────┤
     │                                              ├─ SQLite DB
     │                                              │  (recordings,
     │                                              │   models, history)
     └─ Display results ◀──────────────────────────┘
```

### Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|----------|
| **Frontend** | Vanilla JS + HTML5 | PWA, no frameworks |
| **Styling** | CSS3 | Animations, responsive |
| **Backend** | FastAPI | REST API |
| **AI/ML** | Coqui TTS | Voice cloning |
| **Audio** | Librosa, pydub | Processing |
| **Database** | SQLite | Data storage |
| **ML Framework** | PyTorch | TTS backend |
| **Deployment** | Docker | Containerization |

## 🔐 Privacy & Security

### Data Flow

```
Your Browser → Your Computer → Your Storage → Your Speakers
       ↓              ↓              ↓              ↓
   (HTTPS)      (Local FS)      (SQLite)      (Audio)
       ↓              ↓              ↓              ↓
   [ENCRYPTED]    [YOUR PC]     [YOUR DB]     [YOUR EARS]
                                          ↑
                                    NO CLOUD INVOLVED
```

### What We Don't Do

❌ No telemetry  
❌ No analytics  
❌ No tracking  
❌ No cloud uploads  
❌ No third-party APIs  
❌ No data retention  
❌ No "improvement" of models with your data  

### What We Do

✅ All processing local  
✅ Optional encryption at rest (your choice)  
✅ Open source (auditable)  
✅ GDPR-compliant by design  
✅ HIPAA-compatible (self-hosted)  

## 🧪 Testing

```bash
# Run all tests
uv run pytest tests/ -v

# Run with coverage
uv run pytest tests/ --cov=src/preservemyvoice

# Lint check
uv run ruff check .

# Format code
uv run ruff format .
```

**Test coverage**: 5 unit tests (100% pass rate)

## 📦 Project Structure

```
preservemyvoice/
├── src/preservemyvoice/          # Python source (904 lines)
│   ├── __main__.py              # App entry point
│   ├── config.py                # Settings (Pydantic)
│   ├── logging.py               # Structured logging
│   ├── exceptions.py            # Custom exceptions
│   ├── domain/                  # DB models
│   ├── services/                # Business logic
│   │   ├── audio_processor.py   # Audio handling
│   │   ├── voice_cloner.py      # TTS integration
│   │   └── __init__.py          # VoiceService
│   ├── adapters/                # Infrastructure
│   │   └── __init__.py          # DB session
│   └── api/                     # REST API
│       ├── api.py               # FastAPI router
│       └── __init__.py
├── frontend/                    # PWA frontend
│   ├── index.html               # Single-page app
│   └── dist/                    # Built assets
├── tests/                       # pytest tests
├── Dockerfile                   # Distroless container
├── pyproject.toml               # Dependencies
└── README.md                    # This file
```

## 🎨 Frontend Features

- **Real-time waveform** visualization during recording
- **Animated particle background** (CSS)
- **Responsive design** (mobile + desktop)
- **PWA capable** (installable, offline-ready)
- **No JavaScript frameworks** (vanilla JS only)
- **Accessible** (keyboard navigation, ARIA labels)

## 🌍 Use Cases

### Medical
- **ALS patients** preserving voice before loss
- **Cancer patients** (throat, larynx) pre-surgery
- **Parkinson's** early voice banking
- **MS patients** with speech deterioration

### Personal
- **Legacy creation** for family
- **Content creators** (YouTubers, podcasters)
- **Gamers** (custom voice lines)
- **Artists** (music, voiceovers)

### Institutional
- **Hospitals** (patient care)
- **Speech therapy** clinics
- **Research** (voice studies)
- **Humanitarian** (refugee documentation)

## 🤝 Contributing

We welcome contributions! Areas needing help:

- **Voice model fine-tuning** (improve quality)
- **Additional languages** (multilingual TTS)
- **Mobile apps** (React Native/Flutter wrappers)
- **Accessibility features** (screen readers, etc.)
- **Testing** (integration, E2E)
- **Documentation** (tutorials, guides)

### Development Setup

```bash
# Clone
cd ~/projects

# Install deps
uv sync

# Run tests
uv run pytest tests/ -v

# Run dev server
uv run python -m preservemyvoice

# Lint
uv run ruff check --fix .

# Format
uv run ruff format .
```

## 📄 License

**MIT License** — Free for personal, commercial, and medical use.

```
Copyright (c) 2026 PreserveMyVoice Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

[Standard MIT terms...]
```

## 🙏 Acknowledgments

- **Coqui TTS** — Open source voice AI
- **Librosa** — Audio analysis
- **FastAPI** — Web framework
- **Pydantic** — Settings management
- **SQLAlchemy** — Database ORM

## 📞 Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Join our community discussions
- Read the [contributing guide](CONTRIBUTING.md)

---

**Built with ❤️ for everyone who might lose their voice.**

*Your voice matters. Preserve it.* 🗣️✨
