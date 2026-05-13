import yt_dlp
from pydub import AudioSegment
import os
import subprocess

DOWNLOAD_DIR = 'downloades'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def download_youtube_audio(url: str) -> str:
    """Download audio from YouTube using yt-dlp (works for public videos)."""
    output_template = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
    
    print(f"📥 Downloading audio from: {url}")
    
    # First, try with browser cookies if available
    browsers = ["brave", "chrome", "chromium", "firefox", "edge"]
    
    for browser in browsers:
        try:
            print(f"   Trying {browser} browser...")
            
            cmd = [
                "yt-dlp",
                "--cookies-from-browser", browser,
                "-x",
                "--audio-format", "wav",
                "--audio-quality", "192",
                "-o", output_template,
                url
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print(f"   ✅ Download successful with {browser}!")
                wav_files = [os.path.join(DOWNLOAD_DIR, f) for f in os.listdir(DOWNLOAD_DIR) if f.endswith('.wav')]
                if wav_files:
                    latest_file = max(wav_files, key=os.path.getmtime)
                    return latest_file
                
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
            continue
    
    # Fallback: Try without authentication (works for public videos)
    print("   Trying without authentication...")
    try:
        cmd = [
            "yt-dlp",
            "-x",
            "--audio-format", "wav",
            "--audio-quality", "192",
            "-o", output_template,
            url
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print(f"   ✅ Download successful!")
            wav_files = [os.path.join(DOWNLOAD_DIR, f) for f in os.listdir(DOWNLOAD_DIR) if f.endswith('.wav')]
            if wav_files:
                latest_file = max(wav_files, key=os.path.getmtime)
                return latest_file
    except Exception:
        pass
    
    # All attempts failed
    raise Exception("""
❌ Could not download YouTube video

Possible reasons:
  • Video is private/restricted (needs login)
  • YouTube blocked automated downloads
  • No audio track in video
  • Poor internet connection

Solutions:
  1. Try a PUBLIC video with audio
  2. Install Brave/Chrome with YouTube login for private videos
  3. Test manually: yt-dlp "{url}" -x --audio-format wav
  4. Check if video has audio: yt-dlp -F "{url}"
    """)



def convert_to_wav(input_path: str) -> str:
    """Convert any audio/video file to WAV format using pydub."""
    output_path = os.path.splitext(input_path)[0] + "_converted.wav"
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(16000) #16khz
    audio.export(output_path, format="wav")
    return output_path



def chunk_audio(wav_path : str , chunk_minutes : int = 10) -> list:
    audio = AudioSegment.from_wav(wav_path)
    chunk_ms = chunk_minutes * 60 * 1000 

    chunks = []

    for i, start in enumerate(range(0,len(audio),chunk_ms)):
        chunk = audio[start : start + chunk_ms]
        chunk_path = f"{wav_path}_chunk_{i}.wav"
        chunk.export(chunk_path , format = "wav")

        chunks.append(chunk_path)
    
    return chunks

def process_input(source: str) -> list:
    """
    Process input (YouTube URL or local file) and return chunks.
    For YouTube: Downloads → Converts → Chunks
    For Local: Converts → Chunks
    """
    try:
        if source.startswith("http://") or source.startswith("https://"):
            print("🎥 Detected YouTube URL. Downloading audio...")
            wav_path = download_youtube_audio(source)
        else:
            print("📁 Detected local file. Converting to WAV...")
            if not os.path.exists(source):
                raise FileNotFoundError(f"File not found: {source}")
            wav_path = convert_to_wav(source)

        print("✂️  Chunking audio...")
        chunks = chunk_audio(wav_path)
        print(f"✅ Created {len(chunks)} chunks")
        return chunks
    
    except Exception as e:
        print(f"❌ Error processing input: {str(e)}")
        raise
    print(f"Audio ready — {len(chunks)} chunk(s) created.")
    return chunks


