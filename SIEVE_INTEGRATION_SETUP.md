# PODVOX Sieve Integration - Setup Guide

## 🚀 Branch: `sieve-integration`

This branch contains the complete FastAPI application with Sieve API integration for personalized podcast outreach.

## 📁 Project Structure

```
app/
├── main.py                    # FastAPI application with all endpoints
├── config.py                  # Environment configuration
├── models.py                  # Pydantic request/response models
└── services/
    ├── sieve_service.py       # Sieve Moments & Ask API integration
    └── script_generator.py    # OpenAI script generation

env.example                    # Environment variables template
requirements.txt               # Python dependencies
test_api.py                   # Comprehensive API test suite
```

## 🔧 Quick Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment** 
   ```bash
   cp env.example .env
   # Edit .env with your actual API keys
   ```

3. **Run the application**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

4. **Test the API**
   ```bash
   python test_api.py
   ```

## 🎯 API Endpoints

### Core Workflow Endpoints

- **`POST /generate`** - Complete end-to-end pipeline
  - Input: Prospect name, podcast URL, topic
  - Output: Moments + Context + Generated script

- **`POST /analyze-podcast`** - Sieve analysis workflow
  - Combines Moments + Ask APIs
  - Returns detailed context analysis

### Individual Service Endpoints

- **`POST /extract-moments`** - Sieve Moments API
- **`POST /ask-about-content`** - Sieve Ask API  
- **`POST /generate-script`** - OpenAI script generation

### Utility Endpoints

- **`GET /`** - API information
- **`GET /healthcheck`** - Health status

## 🧪 Testing

The `test_api.py` script tests all endpoints using the sample data:

- Prospect: Steven Bartlett
- Podcast: The Diary of a CEO
- Topic: AI thoughts

```bash
python test_api.py
```

## 📋 Example Workflow

Based on `SampleData/exampleInput.md`:

1. **Extract Moments**: Find clips where Steven discusses AI
2. **Analyze Context**: Get detailed insights about his AI opinions  
3. **Generate Script**: Create personalized 20-second voicenote script
4. **(Future)** Generate voicenote with ElevenLabs

## 🔑 Required Environment Variables

```bash
# OpenAI API Configuration  
OPENAI_API_KEY=sk-proj-your-openai-key-here

# Sieve API Configuration
SIEVE_API_KEY=your-sieve-api-key-here

# ElevenLabs API Configuration (optional for now)
ELEVENLABS_API_KEY=sk_your-elevenlabs-key-here
ELEVENLABS_VOICE_ID=your-voice-id-here

# Application Configuration
APP_NAME=PODVOX
APP_VERSION=0.1.0
DEBUG=True
PORT=8000
```

## 🎉 What's Working

✅ **Sieve Moments API** - Extract podcast moments by topic  
✅ **Sieve Ask API** - Analyze specific content segments  
✅ **OpenAI Integration** - Generate personalized scripts  
✅ **Complete Pipeline** - End-to-end workflow  
✅ **Error Handling** - Comprehensive error management  
✅ **Async Processing** - Using `.push()` pattern recommended by Sieve  
✅ **Comprehensive Testing** - Full test suite  

## 🔜 Next Steps

- [ ] ElevenLabs voice generation integration
- [ ] Database for caching results  
- [ ] Batch processing capabilities
- [ ] Frontend interface integration

## 📖 API Documentation

Once running, visit `http://localhost:8000/docs` for interactive API documentation.

---

Ready to test with real API keys! 🚀 