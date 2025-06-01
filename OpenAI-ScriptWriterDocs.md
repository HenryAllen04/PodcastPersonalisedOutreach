# PODVOX: Personalized Podcast Outreach Engine

## 🚀 Overview

**PODVOX** is a hyper-personalized podcast outreach engine. It automates 1:1 casual outreach to podcast hosts or guests by generating customized voicenotes that reference key moments from their podcast episodes.

Built using:

* **Python** + **FastAPI** (backend framework)
* **Sieve API** (to extract key podcast moments)
* **ElevenLabs API** (voice cloning and TTS)
* **OpenAI API** (script generation)

---

## 📊 Problem Statement

Podcast hosts and guests receive countless cold outreach messages.

**PODVOX** stands out by delivering highly personalized voicenotes that directly reference moments from their own podcast episodes, making outreach more relevant and engaging.

---

## 🧐 Key Features

* ✉️ **Input**:

  * Prospect name
  * Podcast name
  * Podcast episode link

* 🔢 **Context Extraction**:

  * Use Sieve Moments API to extract key moments from the provided podcast episode.

* 💡 **Script Generator**:

  * Personalized outreach script referencing extracted moments dynamically inserting Name and Podcast.

* 🎧 **VoiceNote Generation**:

  * Use pre-cloned ElevenLabs voice ID.
  * Generate an MP3/Ogg personalized voicenote for each prospect.

* 🔗 **Output**:

  * Ready-to-send voicenote file.

* 🏆 **Bonus**:

  * Scale up to batch generation.
  * API endpoint for programmatic voicenote creation.

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

### 4. Script Generator (OpenAI API)

**System Prompt:**

```
You are a personal outreach assistant that creates short, casual, conversational voicenote scripts for podcast outreach.

Your task is to:
- Write in natural, friendly spoken English — as if the user is recording a short, informal voice message.
- Mention the prospect’s first name early in the script.
- Refer to a specific insight or moment from their podcast episode (provided as context).
- Keep it casual, slightly enthusiastic, suggesting a possible collaboration or follow-up.
- Make it sound personal, not scripted, and avoid formal email language.
- End with a light invitation to continue the conversation.

**Formatting Rules**:
- Write in first person.
- Avoid filler phrases like "I hope you're doing well" — get to the point quickly.
- Keep the voicenote under 60 words — concise and snappy.
```

**Example API Call:**

```python
import openai

openai.api_key = "YOUR_OPENAI_API_KEY"

def generate_script(name, context):
    system_prompt = """You are a personal outreach assistant..."""
    user_message = f"Prospect Name: {name}\nPodcast Context: {context}"

    response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=0.8,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    )

    return response['choices'][0]['message']['content']
```

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
| Script Generation   | OpenAI API            |
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
* Add OpenAI integration for dynamic script generation.
