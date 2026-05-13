# 🎬 AI Video Assistant

An intelligent system for analyzing video and audio content using state-of-the-art AI models. This application transcribes videos, generates summaries, extracts key information, and provides RAG-based Q&A capabilities.

## ✨ Features

- **🎙️ Audio Transcription**: Convert video/audio to text using OpenAI Whisper
- **📝 Summarization**: Generate concise summaries of transcribed content
- **🎯 Action Items**: Extract action items from meetings
- **🔑 Key Decisions**: Identify critical decisions made in meetings
- **❓ Question Extraction**: Extract open questions from content
- **🤖 RAG Q&A**: Ask questions about the video content using LangChain RAG
- **🎨 Beautiful UI**: Streamlit-based web interface
- **📥 YouTube Support**: Download and process YouTube videos directly
- **🌐 Multi-language**: Support for English, Hinglish (Hindi-English mix), and more

## 🛠️ Prerequisites

- **Python**: 3.10 or higher
- **FFmpeg**: For audio/video processing
- **API Keys**:
  - Mistral AI (for LLM)
  - (Optional) Sarvam AI (for Hindi/Hinglish transcription)

## 📦 Installation

### 1. Install System Dependencies

#### Ubuntu/Debian:

```bash
sudo apt-get update
sudo apt-get install -y ffmpeg
```

#### macOS:

```bash
brew install ffmpeg
```

#### Windows:

Download from https://ffmpeg.org/download.html

### 2. Install Python Dependencies

```bash
cd /path/to/AI-Video-Assistant-
pip install -r Requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```bash
cp .env .env.local
# Edit .env with your API keys:
```

**`.env` template:**

```
# ─── Mistral AI (Required for LLM) ──────────────────────────────────────────
MISTRAL_API_KEY=your_mistral_api_key_here

# ─── Sarvam AI (Optional - for Hindi/Hinglish transcription) ──────────────────
SARVAM_API_KEY=your_sarvam_api_key_here
SARVAM_STT_MODEL=saaras:v2.5

# ─── Whisper Model Size ────────────────────────────────────────────────────
# Options: tiny, base, small (recommended), medium, large
WHISPER_MODEL=small

# ─── Directory Configuration ───────────────────────────────────────────────
VECTOR_DB_DIR=vector_db
DOWNLOAD_DIR=downloades
```

## 🚀 Getting API Keys

### Mistral AI

1. Visit [Mistral AI Console](https://console.mistral.ai/)
2. Sign up or log in
3. Create an API key in the console
4. Copy the API key to `MISTRAL_API_KEY` in `.env`

### Sarvam AI (Optional)

1. Visit [Sarvam AI](https://sarvam.ai/)
2. Sign up for an account
3. Generate API credentials
4. Copy to `SARVAM_API_KEY` in `.env`

## 🎯 Usage

### Option 1: Web UI (Recommended)

```bash
streamlit run app.py
```

Then open your browser to `http://localhost:8501`

**Features:**

- Upload video/audio files or paste YouTube URLs
- Select language (English, Hindi, Hinglish)
- View real-time transcription and analysis
- Download transcripts, summaries, and reports

### Option 2: Python CLI

```python
from main import run_pipeline

# Process a YouTube URL
result = run_pipeline("https://www.youtube.com/watch?v=...", language="english")

# Or process a local file
result = run_pipeline("/path/to/audio.mp3", language="english")

# Access results
print(f"Title: {result['title']}")
print(f"Summary: {result['summary']}")
print(f"Action Items: {result['action_items']}")
print(f"Key Decisions: {result['key_decisions']}")
print(f"Open Questions: {result['open_questions']}")

# Use RAG chain for Q&A
rag_chain = result['rag_chain']
answer = rag_chain.invoke("What were the main topics discussed?")
print(f"Answer: {answer}")
```

### Option 3: Direct Python Import

```python
from core.transcriber import transcribe_all
from core.summarizer import summarize, generate_title
from core.extractor import extract_action_items, extract_key_decisions
from utils.audio_processor import process_input

# 1. Process input (YouTube URL or local file)
chunks = process_input("https://www.youtube.com/watch?v=...")

# 2. Transcribe
transcript = transcribe_all(chunks, language="english")

# 3. Generate insights
title = generate_title(transcript)
summary = summarize(transcript)
actions = extract_action_items(transcript)
decisions = extract_key_decisions(transcript)
```

## 📁 Project Structure

```
AI-Video-Assistant-/
├── app.py                  # Streamlit web application
├── main.py                 # CLI entry point
├── Requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this)
├── .gitignore             # Git ignore rules
├── core/
│   ├── transcriber.py     # Whisper & Sarvam STT integration
│   ├── summarizer.py      # LLM-based summarization
│   ├── extractor.py       # Action items, decisions, questions
│   ├── rag_engine.py      # RAG pipeline with LangChain
│   └── vector_store.py    # ChromaDB vector database
└── utils/
    └── audio_processor.py # Audio/video download & processing
```

## 🔧 Configuration

### Whisper Models

| Model  | Speed  | Accuracy   | Memory | Use Case        |
| ------ | ------ | ---------- | ------ | --------------- |
| tiny   | ⚡⚡⚡ | ⭐         | 1GB    | Quick testing   |
| base   | ⚡⚡   | ⭐⭐       | 1GB    | Fast processing |
| small  | ⚡     | ⭐⭐⭐     | 2GB    | **Recommended** |
| medium | -      | ⭐⭐⭐⭐   | 5GB    | High accuracy   |
| large  | -      | ⭐⭐⭐⭐⭐ | 10GB   | Best accuracy   |

### RAG Configuration

Located in `core/vector_store.py`:

- **Embedding Model**: `all-MiniLM-L6-v2` (fast, efficient)
- **Vector DB**: ChromaDB (local, no external service)
- **Chunk Size**: 500 tokens
- **Retrieval K**: 4 chunks

Modify for better accuracy:

```python
EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"  # More accurate
CHUNK_SIZE = 1000  # Larger chunks
```

## ⚙️ Troubleshooting

### FFmpeg not found

```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
# Add to PATH
```

### CUDA/GPU Issues

To run on CPU only:

```bash
export CUDA_VISIBLE_DEVICES=""
streamlit run app.py
```

### Out of Memory

1. Use smaller Whisper model: `WHISPER_MODEL=tiny` or `base`
2. Process shorter audio files (< 1 hour)
3. Reduce batch size in config

### Slow Transcription

1. Use GPU if available (NVIDIA GPU with CUDA)
2. Use smaller Whisper model
3. Check internet connection (for downloading models first time)

### API Errors

1. Verify API keys in `.env`
2. Check API rate limits
3. Ensure internet connection
4. Review error logs in terminal

## 📊 Performance Metrics

**Typical Processing Times** (small model):

| Task                               | Duration     |
| ---------------------------------- | ------------ |
| 1-hour audio transcription         | 5-10 minutes |
| Summary generation                 | 30 seconds   |
| Key extraction (actions/decisions) | 20 seconds   |
| RAG indexing                       | 1 minute     |
| Q&A response                       | 2-5 seconds  |

**Memory Usage:**

- Base: ~2GB RAM
- With Whisper (small): ~4GB RAM
- With ChromaDB + Transformers: ~6GB RAM

## 🔐 Security Notes

- Never commit `.env` files with real API keys
- Use environment-specific `.env.local` files
- Rotate API keys periodically
- Keep dependencies updated

## 📚 Technologies Used

- **LLM**: Mistral AI (via LangChain)
- **STT**: OpenAI Whisper
- **RAG**: LangChain + ChromaDB
- **Embeddings**: Sentence Transformers (HuggingFace)
- **UI**: Streamlit
- **Audio**: pydub, FFmpeg
- **Vector DB**: ChromaDB
- **Video Download**: yt-dlp

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

## 🙋 Support

For issues and questions:

1. Check the Troubleshooting section
2. Review error logs
3. Open an GitHub issue with:
   - Error message
   - Python version
   - OS information
   - Steps to reproduce

## 🚧 Roadmap

- [ ] Support for video file uploads
- [ ] Real-time transcription streaming
- [ ] Multiple language batch processing
- [ ] Export to different formats (PDF, DOCX, JSON)
- [ ] Speaker diarization
- [ ] Sentiment analysis
- [ ] Custom domain fine-tuning
- [ ] API server mode

---

**Created with ❤️ for better video analysis**
