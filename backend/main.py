from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import math, os, random, shutil, uuid, wave
from datetime import datetime
from typing import Optional
import requests

app = FastAPI(title="Private Music Studio")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
GENERATED_DIR = BASE_DIR / "generated"
UPLOAD_DIR.mkdir(exist_ok=True)
GENERATED_DIR.mkdir(exist_ok=True)

app.mount("/generated", StaticFiles(directory=str(GENERATED_DIR)), name="generated")

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")


def get_default_lyrics(title: str, genre: str, mood: str, theme: str, language: str) -> str:
    if language.lower() == "swahili":
        return f"""
{title}

Genre: {genre}
Mood: {mood}

Nimekuja kwa roho ya {mood.lower()}, nikikumbuka {theme},
Moyo wangu unaimba kwenye kiza na nuru,
Ninapenda safari ya ndoto na upendo,
Kila pigo la moyo linaanza kwa jina lako.

Chorus:
{theme} ni moto ndani ya moyo wangu,
Ninakuimba kwa sauti ya furaha,
Na kila hatua ya maisha ina rekodi yako,
Njia yangu ni nyimbo, na wewe ni sehemu ya moyo.

Verse 2:
Nimefanya dunia kuzunguka kwa tabasamu,
Kila usiku unataka kufika kwako,
Nitakutafuta kwa kila pigo la moyo,
Na kila kioo kinatoka kwenye lengo lako.

Bridge:
Kama mvua itanyesha, nitakuimba,
Kama upepo utatupa, nitakutafuta,
Wimbo wangu ni njia ya roho yangu,
Na {theme} ni shairi la maisha yangu.
""".strip()

    return f"""
Title: {title}
Genre: {genre}
Mood: {mood}

I carry {theme} like a hidden flame,
A melody in my chest, a rhythm in my name,
Every beat is a memory, every line is a prayer,
And every heartbeat says you are still there.

Chorus:
{theme} is the fire inside my soul,
The rhythm of my heart, the glow in my goal,
I sing it into the morning, I sing it into the night,
And I let the music carry me back to life.

Verse 2:
The city hums in my ears,
The night folds into a dream,
I move with the pulse of this sound,
And somehow your love is still my guide.

Bridge:
When the road gets long, I hold the beat,
When the night feels heavy, I still believe,
This song is my shelter, this song is my truth,
And {theme} is the voice I trust.
""".strip()


def generate_beat_wav(file_path: str, style: str = "strings", duration_seconds: int = 30, sample_rate: int = 22050):
    total_samples = sample_rate * duration_seconds
    amplitude = 32767

    style_map = {
        "strings": {"base_freq": 120, "harmonic": 0.33, "noise": 0.10},
        "benga": {"base_freq": 95, "harmonic": 0.40, "noise": 0.12},
        "afrobeat": {"base_freq": 110, "harmonic": 0.25, "noise": 0.15},
        "acoustic": {"base_freq": 140, "harmonic": 0.22, "noise": 0.08},
        "soul": {"base_freq": 130, "harmonic": 0.35, "noise": 0.09},
    }
    cfg = style_map.get(style.lower(), style_map["strings"])

    beat_interval = 0.30
    with wave.open(file_path, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)

        frames = []
        for i in range(total_samples):
            t = i / sample_rate

            kick = 0.0
            if (t % beat_interval) < 0.09:
                kick = math.sin(2 * math.pi * 50 * t) * 0.9

            pad = math.sin(2 * math.pi * cfg["base_freq"] * t) * 0.26
            harmonic = math.sin(2 * math.pi * (cfg["base_freq"] * 2.0) * t) * cfg["harmonic"]

            noise = 0.0
            if int(t * 8) != int((t - 0.001) * 8):
                noise = random.uniform(-1, 1) * cfg["noise"]

            val = (kick + pad + harmonic + noise) * amplitude
            frames.append(int(max(-32768, min(32767, val))))

        wav_file.writeframes(
            b"".join(int(v).to_bytes(2, byteorder="little", signed=True) for v in frames)
        )


def simple_voice_like_wave(file_path: str, lyrics: str, duration_seconds: int = 30, sample_rate: int = 22050):
    total_samples = sample_rate * duration_seconds
    amplitude = 20000
    words = lyrics.split()
    if not words:
        words = ["hello", "my", "song"]

    with wave.open(file_path, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        frames = []

        for i in range(total_samples):
            t = i / sample_rate
            idx = min(len(words) - 1, int((i / total_samples) * len(words)))
            base = 170 + (ord(words[idx][0]) % 40)
            vibrato = math.sin(2 * math.pi * 6 * t) * 8
            voice = math.sin(2 * math.pi * (base + vibrato) * t) * 0.7
            mod = math.sin(2 * math.pi * 2.5 * t) * 0.3
            val = (voice + mod) * amplitude
            frames.append(int(max(-32768, min(32767, val))))

        wav_file.writeframes(
            b"".join(int(v).to_bytes(2, byteorder="little", signed=True) for v in frames)
        )


def mix_two_wavs(beat_file: str, voice_file: str, output_file: str):
    with wave.open(beat_file, "rb") as beat, wave.open(voice_file, "rb") as voice:
        if beat.getnchannels() != voice.getnchannels():
            raise ValueError("Different channel counts")
        if beat.getframerate() != voice.getframerate():
            raise ValueError("Different sample rates")

        frames1 = beat.readframes(beat.getnframes())
        frames2 = voice.readframes(voice.getnframes())

        final_frames = []
        for i in range(min(len(frames1), len(frames2))):
            left = int.from_bytes(frames1[i:i+2], byteorder="little", signed=True)
            right = int.from_bytes(frames2[i:i+2], byteorder="little", signed=True)
            mixed = int((left * 0.72) + (right * 0.88))
            mixed = max(-32768, min(32767, mixed))
            final_frames.append(mixed.to_bytes(2, byteorder="little", signed=True))

        with wave.open(output_file, "wb") as out:
            out.setnchannels(1)
            out.setsampwidth(2)
            out.setframerate(beat.getframerate())
            out.writeframes(b"".join(final_frames))


def elevenlabs_generate_voice(prompt_text: str, output_path: str, voice_id: str = None, api_key: str = None):
    if not api_key or not voice_id:
        return False

    headers = {
        "Content-Type": "application/json",
        "xi-api-key": api_key,
    }
    payload = {
        "text": prompt_text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.7,
        },
    }

    try:
        response = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
            json=payload,
            headers=headers,
            timeout=60,
        )
        if response.status_code != 200:
            return False

        with open(output_path, "wb") as f:
            f.write(response.content)
        return True
    except Exception:
        return False


def save_uploaded_voice(upload_file: Optional[UploadFile], output_dir: Path) -> Optional[str]:
    if upload_file is None or upload_file.filename is None:
        return None
    ext = os.path.splitext(upload_file.filename)[1] or ".wav"
    name = f"{uuid.uuid4().hex}{ext}"
    path = output_dir / name
    with path.open("wb") as f:
        shutil.copyfileobj(upload_file.file, f)
    return str(path)


@app.get("/")
def home():
    return {"message": "Private AI Music Studio is running"}


@app.get("/api/health")
def health():
    return {"ok": True}


@app.post("/api/generate-song")
async def generate_song(
    title: str = Form("My Song"),
    genre: str = Form("Afrobeat"),
    mood: str = Form("Happy"),
    theme: str = Form("love"),
    language: str = Form("Swahili"),
    style: str = Form("strings"),
    duration: int = Form(30),
    lyrics: str = Form(""),
    voice_file: Optional[UploadFile] = File(None),
):
    saved_voice_path = save_uploaded_voice(voice_file, UPLOAD_DIR)
    final_lyrics = lyrics.strip() or get_default_lyrics(title, genre, mood, theme, language)

    beat_file = GENERATED_DIR / f"{uuid.uuid4().hex}.wav"
    generate_beat_wav(str(beat_file), style=style, duration_seconds=duration)

    voice_file_path = GENERATED_DIR / f"{uuid.uuid4().hex}-voice.wav"
    voice_generated = False
    if ELEVENLABS_API_KEY and ELEVENLABS_VOICE_ID:
        voice_generated = elevenlabs_generate_voice(
            prompt_text=final_lyrics,
            output_path=str(voice_file_path),
            voice_id=ELEVENLABS_VOICE_ID,
            api_key=ELEVENLABS_API_KEY,
        )

    if not voice_generated:
        simple_voice_like_wave(str(voice_file_path), final_lyrics, duration_seconds=max(10, duration))

    final_output = GENERATED_DIR / f"{uuid.uuid4().hex}-final.wav"
    mix_two_wavs(str(beat_file), str(voice_file_path), str(final_output))

    return {
        "title": title,
        "genre": genre,
        "mood": mood,
        "theme": theme,
        "language": language,
        "style": style,
        "duration": duration,
        "lyrics": final_lyrics,
        "audio_url": f"http://localhost:8000/generated/{final_output.name}",
        "voice_status": "Human-like voice synthesis enabled" if voice_generated else "Fallback voice layer active",
        "voice_uploaded": saved_voice_path is not None,
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }
