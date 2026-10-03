# Private AI Music Studio - Upgraded

Advanced browser-based personal music studio with voice synthesis, song history, and MP3 export.

## Features
- **Personal Studio**: Private music creation workspace
- **Custom Lyrics**: Write your own or auto-generate
- **Voice Upload**: Upload your voice sample for personalized output
- **Style Selection**: strings, benga, afrobeat, acoustic, soul
- **Song History**: Save and reload past creations
- **MP3 Export**: Download songs in MP3 format (with ffmpeg)
- **Human-like Voice**: Optional ElevenLabs integration
- **Real-time Preview**: Play and edit before download

## Stack
- Frontend: React + Vite
- Backend: Python + FastAPI
- Audio: WAV generation, mixing, MP3 conversion
- Voice API: ElevenLabs (optional)
- Storage: Local JSON history

## Quick Start

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

Open: http://localhost:5173

## ElevenLabs Setup (Optional)
```bash
export ELEVENLABS_API_KEY="your_key_here"
export ELEVENLABS_VOICE_ID="your_voice_id_here"
```

## Notes
- This is a personal/private MVP
- Song history stored in `backend/history.json`
- FFmpeg required for MP3 export (optional)
- Works without voice API using fallback synth
