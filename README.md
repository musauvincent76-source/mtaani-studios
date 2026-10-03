# Private AI Music Studio

This project is a browser-based personal music studio for creating songs using custom lyrics, optional voice upload, and a warm string / benga / Afro-inspired beat.

## Features
- personal/private song studio
- custom lyrics input
- optional voice upload
- style selection (strings / benga / afrobeat / acoustic / soul)
- final generated song preview and download
- optional ElevenLabs integration for more human-like voice output

## Stack
- Frontend: React + Vite
- Backend: Python + FastAPI
- Audio: Python WAV generation and mixing
- Optional voice API: ElevenLabs

## Project structure

- `backend/main.py`
- `backend/requirements.txt`
- `backend/.env.example`
- `frontend/package.json`
- `frontend/index.html`
- `frontend/src/main.jsx`
- `frontend/src/App.jsx`
- `frontend/src/styles.css`

## Run locally

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Then open:
```text
http://localhost:5173
```

## Optional voice API setup
Create environment variables for ElevenLabs:
```bash
export ELEVENLABS_API_KEY="your_api_key_here"
export ELEVENLABS_VOICE_ID="your_voice_id_here"
```

If those are not set, the app still works using a fallback voice-like synth.

## Notes
This is a personal/private MVP. It is designed for your own music creation workflow rather than a public audience product.
