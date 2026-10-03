import { useState } from "react";

const initialForm = {
  title: "My Personal Song",
  genre: "Afrobeat",
  mood: "Happy",
  theme: "love",
  language: "Swahili",
  style: "strings",
  duration: 30
};

function App() {
  const [form, setForm] = useState(initialForm);
  const [lyrics, setLyrics] = useState("");
  const [voiceFile, setVoiceFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const formData = new FormData();
      Object.entries(form).forEach(([key, value]) => {
        formData.append(key, value);
      });
      formData.append("lyrics", lyrics);
      if (voiceFile) {
        formData.append("voice_file", voiceFile);
      }

      const response = await fetch("http://localhost:8000/api/generate-song", {
        method: "POST",
        body: formData
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || "Something went wrong");
      }

      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-shell">
      <div className="panel">
        <h1>My Private Song Studio</h1>
        <p className="subtitle">Your own lyrics + your own voice + warm string vibe</p>

        <form className="song-form" onSubmit={handleSubmit}>
          <div className="field">
            <label>Song Title</label>
            <input name="title" value={form.title} onChange={handleChange} />
          </div>

          <div className="grid">
            <div className="field">
              <label>Genre</label>
              <select name="genre" value={form.genre} onChange={handleChange}>
                <option>Afrobeat</option>
                <option>Amapiano</option>
                <option>Benga</option>
                <option>Gospel</option>
                <option>Pop</option>
                <option>Soul</option>
              </select>
            </div>

            <div className="field">
              <label>Mood</label>
              <select name="mood" value={form.mood} onChange={handleChange}>
                <option>Happy</option>
                <option>Sad</option>
                <option>Romantic</option>
                <option>Chill</option>
                <option>Energetic</option>
              </select>
            </div>
          </div>

          <div className="grid">
            <div className="field">
              <label>Theme</label>
              <input name="theme" value={form.theme} onChange={handleChange} />
            </div>

            <div className="field">
              <label>Language</label>
              <select name="language" value={form.language} onChange={handleChange}>
                <option>Swahili</option>
                <option>English</option>
                <option>Sheng</option>
              </select>
            </div>
          </div>

          <div className="grid">
            <div className="field">
              <label>Style</label>
              <select name="style" value={form.style} onChange={handleChange}>
                <option>strings</option>
                <option>benga</option>
                <option>afrobeat</option>
                <option>acoustic</option>
                <option>soul</option>
              </select>
            </div>

            <div className="field">
              <label>Duration (sec)</label>
              <input
                type="number"
                name="duration"
                min="10"
                max="120"
                value={form.duration}
                onChange={handleChange}
              />
            </div>
          </div>

          <div className="field">
            <label>Lyrics (optional)</label>
            <textarea
              value={lyrics}
              onChange={(e) => setLyrics(e.target.value)}
              rows={8}
              placeholder="Type your own lyrics here..."
            />
          </div>

          <div className="field">
            <label>Upload your voice sample (optional)</label>
            <input
              type="file"
              accept=".wav,.mp3,.m4a,.ogg"
              onChange={(e) => setVoiceFile(e.target.files?.[0] || null)}
            />
          </div>

          <button type="submit" disabled={loading}>
            {loading ? "Generating..." : "Generate Song"}
          </button>
        </form>

        {error && <div className="error-box">{error}</div>}

        {result && (
          <div className="result-box">
            <h2>{result.title}</h2>
            <div className="meta">
              <span>{result.genre}</span>
              <span>{result.mood}</span>
              <span>{result.language}</span>
              <span>{result.style}</span>
              <span>{result.duration}s</span>
            </div>

            <audio controls src={result.audio_url} className="audio-player" />

            <div className="status-line">
              <strong>Voice:</strong> {result.voice_status}
            </div>

            <div className="lyrics-box">
              <h3>Lyrics</h3>
              <pre>{result.lyrics}</pre>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
