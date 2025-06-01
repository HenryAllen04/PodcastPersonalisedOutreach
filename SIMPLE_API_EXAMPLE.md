# PODVOX Simple API

## 🎯 Super Simple Interface

Just **2 inputs** needed:

1. **Topic** - what to search for
2. **Video URL** - YouTube/podcast link

## 🚀 Example Usage

### cURL
```bash
curl -X POST "http://localhost:8000/generate-voicenote-simple" \
  -d "topic=AI thoughts" \
  -d "video_url=https://www.youtube.com/watch?v=u0o3IlsEQbI"
```

### Python
```python
import requests

response = requests.post(
    "http://localhost:8000/generate-voicenote-simple",
    params={
        "topic": "AI thoughts",
        "video_url": "https://www.youtube.com/watch?v=u0o3IlsEQbI"
    }
)

result = response.json()
print(f"Script: {result['generated_script']}")
print(f"Download: {result['voicenote']['download_url']}")
```

### JavaScript
```javascript
const response = await fetch('http://localhost:8000/generate-voicenote-simple', {
  method: 'POST',
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  body: new URLSearchParams({
    topic: 'AI thoughts',
    video_url: 'https://www.youtube.com/watch?v=u0o3IlsEQbI'
  })
});

const result = await response.json();
console.log('Script:', result.generated_script);
console.log('Download:', result.voicenote.download_url);
```

## 📊 Response Format

```json
{
  "success": true,
  "topic": "AI thoughts",
  "video_url": "https://www.youtube.com/watch?v=u0o3IlsEQbI",
  "generated_script": "Hey there, your take on AGI being just 2 years away really caught my attention...",
  "script_word_count": 45,
  "moments_found": 1,
  "voicenote": {
    "filename": "voicenote_AI_thoughts_1733012345.mp3",
    "download_url": "/download-voicenote/voicenote_AI_thoughts_1733012345.mp3"
  }
}
```

## 🎯 Different Topics Examples

| Topic | Description |
|-------|-------------|
| `"AI thoughts"` | Find AI/technology discussions |
| `"productivity"` | Productivity tips and hacks |
| `"entrepreneurship"` | Business and startup advice |
| `"personal growth"` | Self-improvement content |
| `"investing"` | Investment and finance talk |

## ⚡ Processing Time

- **Sieve Analysis**: ~2 minutes (finds exact moments)
- **Script Generation**: ~5 seconds (OpenAI GPT-4)
- **Voice Synthesis**: ~10 seconds (ElevenLabs)
- **Total**: ~2-3 minutes

## 🎧 Output

- **High-quality MP3** voicenote ready for outreach
- **<60 words** personalized script
- **References specific content** from the podcast
- **Download link** for immediate use 