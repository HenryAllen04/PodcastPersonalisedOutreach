# PODVOX: Personalized Podcast Outreach Engine

## 🚀 Overview

**PODVOX** is a hyper-personalized podcast outreach engine. It automates 1:1 casual outreach to podcast hosts or guests by generating customized voicenotes that reference key moments from their podcast episodes.

Built using:

* **Python** + **FastAPI** (backend framework)
* **React** + **TypeScript** + **Tailwind CSS** (frontend interface)
* **Sieve API** (to extract key podcast moments)
* **ElevenLabs API** (voice cloning and TTS)

---

## 🎯 New Frontend Interface

We've added a beautiful, modern frontend interface that allows users to:

- Input podcast URLs with smart validation
- Enter recipient details
- Track processing progress in real-time
- Download generated MP4 voicenotes
- See visual feedback throughout the process

### Frontend Tech Stack
- **React 18** with TypeScript
- **Vite** for fast development
- **Tailwind CSS** for modern styling
- **Lucide React** for icons
- **Axios** for API communication

### Quick Start - Frontend
```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:5173`

---

## 📊 Problem Statement

Podcast hosts and guests receive countless cold outreach messages.

**PODVOX** stands out by delivering highly personalized voicenotes that directly reference moments from their own podcast episodes, making outreach more relevant and engaging.

---

## 🎯 Key Features

* **Smart Moment Extraction**: Uses Sieve's Moments API to find specific topics (e.g., childhood stories, key insights)
* **Detailed Content Analysis**: Uses Sieve's Ask API to analyze specific timestamp ranges
* **Personalized Scripts**: Generates contextual outreach messages based on actual podcast content
* **Voice Generation**: Creates natural-sounding voicenotes using ElevenLabs (coming soon)

---

## 🔹 MVP Development Plan (High-Level)

### 1. Project Setup

* Initialize Python project.
* Set up **FastAPI** app with endpoints.
* Create environment variables for API keys.

### 2. Basic Prospect Intake

* Define endpoint to submit:

  * Name
  * Podcast name
  * Podcast episode URL

### 3. Sieve API Integration

* Query the podcast episode URL.
* Extract key moments and summaries.

### 4. Script Generator

* Templated script:

  ```
  "Hey {name}, I listened to your recent episode of {podcast_name} where you talked about [key moment]. It really resonated with me. Would love to connect and share some thoughts."
  ```
* Add more prompt templates for diversity.

### 5. ElevenLabs Integration

* API call to generate audio using:

  * Provided cloned voice ID.
  * Generated script.
* Return audio file.

### 6. Hosting / Response

* Serve voicenote file via temporary URL.
* Or allow download.

---

## 🚶️ End-to-End User Flow

1. Submit prospect data (Name + Podcast Name + Episode URL).
2. System extracts key podcast moments.
3. System generates personalized outreach script.
4. System generates a voicenote with cloned voice.
5. Return voicenote ready for outreach.

---

## 💰 Tech Stack

| Component           | Tech/Service          |
| ------------------- | --------------------- |
| Backend API         | Python + FastAPI      |
| Context Extraction  | Sieve Moments API     |
| Voice Cloning & TTS | ElevenLabs API        |
| Hosting (Optional)  | VEED / S3 (if needed) |

---

## 🏆 Judging Criteria Alignment

* **Creativity**: AI-powered 1:1 podcast outreach via personalized voicenotes.
* **Impact**: Higher engagement from personalized references to prospect's podcast.
* **Usability & Execution**: Simple API + Live Demo.
* **Presentation**: Showcase 2-3 real voicenotes.

---

## 💡 Bonus Extensions (Post MVP)

* Dynamic tone selection (casual, formal, etc).
* Batch processing for CSV prospect lists.
* Subtitles and transcription.

---

## 🔧 API Endpoints Sketch

| Method | Endpoint     | Description                         |
| ------ | ------------ | ----------------------------------- |
| POST   | /generate    | Submit prospect data, get voicenote |
| GET    | /healthcheck | Service status                      |

---

## 📚 How to Run (Development)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run FastAPI app
uvicorn app.main:app --reload
```

---

Ready to change the game of personalized podcast outreach! 🚀

---

## 🔔 Notes

* If time is limited, focus first on **VoiceNote-only MVP**.
* **Cloned ElevenLabs voice ID** is pre-integrated for realism.

---

**Next Steps**:

* Set up basic FastAPI scaffold.
* Integrate Sieve Moments API.
* Start with simple voicenote generation endpoint.

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd ContextualisedVoicenotes
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp env.example .env
   # Edit .env and add your API keys:
   # - SIEVE_API_KEY (required)
   # - ELEVENLABS_API_KEY (optional for now)
   ```

5. **Run the application**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

## 📖 API Endpoints

### 1. Extract Moments
Find key moments from a podcast episode.

```bash
POST /extract-moments
{
  "podcast_url": "https://www.youtube.com/watch?v=...",
  "queries": ["childhood stories", "key insights"],
  "min_clip_length": 10.0
}
```

### 2. Analyze Childhood Moments (Complete Workflow)
Demonstrates the full Moments → Ask pipeline.

```bash
POST /analyze-childhood-moments
{
  "prospect_name": "Steven Bartlett",
  "podcast_url": "https://www.youtube.com/watch?v=sFkR34AMPw8"
}
```

This endpoint:
1. **Finds moments** where childhood is discussed
2. **Asks detailed questions** about those specific timestamps
3. **Generates personalized outreach** based on the content

### 3. Generate Voicenote (Full Pipeline)
Complete end-to-end voicenote generation.

```bash
POST /generate
{
  "prospect_name": "John Doe",
  "podcast_name": "The Example Podcast",
  "podcast_url": "https://...",
  "tone": "casual"
}
```

## 🔧 Technical Implementation

### Sieve Integration (IMPORTANT)

**Key Learning**: Use `.push()` instead of `.run()` for async operations!

```python
# ✅ CORRECT - Async pattern recommended by Sieve CTO
job = sieve_function.push(video, prompt, ...)
result = job.result()  # This blocks until complete

# ❌ WRONG - Can cause timeouts on long videos
result = sieve_function.run(video, prompt, ...)
```

### Workflow Example

```python
# 1. Find moments about childhood
moments = await sieve_service.extract_key_moments(
    podcast_url="https://youtube.com/...",
    queries=["childhood stories"],
    min_clip_length=15.0
)

# 2. Get detailed insights from specific timestamps
insights = await sieve_service.ask_about_moments(
    podcast_url="https://youtube.com/...",
    questions=["What childhood story is shared here?"],
    start_time=5862.84,  # From moments result
    end_time=5884.84
)

# 3. Generate personalized outreach
# Result: "I was moved by your story about climbing a mountain at night..."
```

## 🧪 Testing

Run the test script to verify Sieve integration:

```bash
python test_sieve_integration.py
```

Expected output:
```
✅ Found 1 childhood-related moments!
🎬 Childhood Moments Discovered:
  1. [97:42] Duration: 22.0s
✅ Got insights for moment 1!
   A: The video features a man recounting a childhood experience...
```

## 📁 Project Structure

```
ContextualisedVoicenotes/
├── app/
│   ├── main.py              # FastAPI application
│   ├── config.py             # Configuration management
│   └── services/
│       ├── sieve_service.py  # Sieve API integration
│       └── script_generator.py # Script generation logic
├── test_sieve_integration.py # Integration tests
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
└── README.md                # This file
```

## 🔑 Environment Variables

```bash
# Required
SIEVE_API_KEY=your_sieve_api_key_here

# Optional (for future features)
ELEVENLABS_API_KEY=your_elevenlabs_key_here
ELEVENLABS_VOICE_ID=voice_id_here
```

## 🎯 Use Cases

1. **Sales Outreach**: Reference specific moments from a prospect's podcast appearance
2. **Networking**: Create personalized connection requests based on shared experiences
3. **Research**: Extract and analyze specific topics across multiple podcasts
4. **Content Creation**: Find and compile moments about specific themes

## 🚧 Current Status

- ✅ Sieve Moments API integration (finds topic timestamps)
- ✅ Sieve Ask API integration (analyzes specific segments)
- ✅ Personalized script generation
- ✅ FastAPI endpoints
- 🔄 ElevenLabs voice generation (coming soon)
- 🔄 Database for caching results (planned)

## 🐛 Troubleshooting

### "Job Canceled" errors
- Usually happens with long videos (>1 hour)
- Solution: Use shorter test videos or implement chunking

### Import errors
- Make sure you have `pip install sievedata`
- Import as: `import sieve` (not `import sievedata as sieve`)

### Timeout issues
- Ensure you're using `.push()` not `.run()` for Sieve APIs
- Check your internet connection for large video downloads

## 📄 License

[Your license here]

## 🤝 Contributing

[Your contributing guidelines here]

## 🚀 Features

### Enhanced Sieve Integration ✨ NEW
- **Comprehensive Hardship Analysis**: Advanced AI-powered analysis of podcast episodes
- **Two-Phase Pipeline**: Moments discovery → Deep insights extraction
- **Structured Prompts**: Markdown-formatted analysis for consistent results
- **Personalized Outreach**: Automatic generation of custom outreach scripts
- **Real-time Processing**: Optimized for fast, production-ready workflows

[📖 **Read the Complete Sieve Integration Guide**](docs/SIEVE_INTEGRATION_GUIDE.md)

### Core Capabilities
- 🎯 **Intelligent Moment Discovery**: Find specific hardship stories and vulnerable moments
- 🤖 **Deep Content Analysis**: Extract actionable insights with structured prompts
- 📝 **Outreach Script Generation**: Create personalized messages based on discovered content
- 🔊 **Voice Note Creation**: Convert scripts to natural-sounding audio messages
- 📊 **Comprehensive Logging**: Track every step of the analysis workflow

## 🛠 APIs

### Sieve Integration Endpoints
- `POST /analyze-hardship-moments` - Complete hardship analysis workflow
- `POST /extract-moments` - Basic moment extraction
- `POST /generate` - Full voicenote generation pipeline

### Example Usage
```bash
# Analyze hardship moments in a podcast
curl -X POST "http://localhost:8000/analyze-hardship-moments" \
  -H "Content-Type: application/json" \
  -d '{
    "podcast_url": "https://youtube.com/watch?v=example",
    "prospect_name": "Steven Bartlett"
  }'
```

## 🧪 Testing

Test the comprehensive Sieve integration:
```bash
python test_comprehensive_queries.py
```

This demonstrates:
- Single comprehensive Moments API query
- Structured markdown Ask API prompts  
- Step-by-step workflow logging
- Complete analysis pipeline

## 📚 Documentation

- [📖 Sieve Integration Guide](docs/SIEVE_INTEGRATION_GUIDE.md) - Complete technical documentation
- [🔧 API Reference](docs/API.md) - Endpoint documentation
- [⚙️ Configuration](docs/CONFIG.md) - Setup and configuration guide
