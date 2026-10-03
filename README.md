# Private AI Music Studio

A personal music creation studio for generating warm Afro-inspired songs, custom lyrics, and local audio mixes with optional voice synthesis support.

This project is designed as a private/local creative tool and can also be showcased publicly without requiring real API credentials.

## Features
- Personal music studio interface
- Input title, genre, mood, theme, language, style, and duration
- Custom or auto-generated lyrics
- Optional uploaded voice sample
- Local beat generation + voice-like layer mix
- Song history panel for previously generated tracks
- Downloadable audio output
- Optional ElevenLabs integration for better voice quality
- Built to work even without any external API key

## Tech Stack
- Frontend: React + Vite
- Backend: Python + FastAPI
- Audio processing: Python WAV generation and mixing
- Optional voice synthesis: ElevenLabs
- Local storage: JSON history file

## Project Structure
- `backend/main.py` — FastAPI app and audio generation logic
- `backend/requirements.txt` — Python dependencies
- `backend/.env.example` — sample env file
- `frontend/package.json` — frontend config
- `frontend/src/App.jsx` — main UI logic
- `frontend/src/styles.css` — styling
- `README.md` — project overview

## Run Locally

### 1. Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Frontend
```bash
cd frontend
npm install
npm run dev
```

Then open:
```text
http://localhost:5173
```

## Optional Voice Setup
If you want stronger voice synthesis, optionally set these environment variables:

```bash
export ELEVENLABS_API_KEY="your_api_key_here"
export ELEVENLABS_VOICE_ID="your_voice_id_here"
```

If those values are not set, the app still works using a built-in fallback voice-like synth.

## Public-Safe Notes
This project is safe to use as a public demo because:
- no real API credentials are required for normal use
- `.env` is ignored by git
- no sensitive keys are included in the repository by default
- external services are optional only

## Notes
This is a private/local creative MVP designed for personal music creation. It is intentionally simple, functional, and easy to extend later with more advanced audio tools, cloud storage, or user accounts.

## License
This project is provided as a personal demo project for music studio experimentation and learning.
