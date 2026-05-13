import whisper
import os
from deep_translator import GoogleTranslator

WHISPER_MODEL = os.getenv("WHISPER_MODEL", "small")

_model = None


def load_model():

    global _model  

    if _model is None: 
        print(f"Loading Whisper model: {WHISPER_MODEL} ...")
        _model = whisper.load_model(WHISPER_MODEL) 
        print("Whisper model loaded.")
    return _model 


def transcribe_chunk_whisper(chunk_path: str) -> str:
    """Transcribe audio using Whisper (works for any language)."""
    model = load_model()  
    result = model.transcribe(chunk_path, task="transcribe")  
    return result["text"]


def translate_to_english(text: str, source_language: str = "hi") -> str:
    """
    Translate text to English using Google Translate.
    
    Args:
        text: Text to translate
        source_language: Language code (default 'hi' for Hindi)
    
    Returns:
        Translated text in English
    """
    if not text.strip():
        return ""
    
    try:
        translator = GoogleTranslator(source_language=source_language, target_language='en')
        translated = translator.translate(text)
        return translated
    except Exception as e:
        print(f"⚠️  Translation failed: {e}. Returning original text.")
        return text

   



def transcribe_chunk(chunk_path: str, language: str = "english") -> str:
    """
    Transcribe one chunk using Whisper, optionally translate to English.
    
    - english  → Whisper (transcribe as English)
    - hinglish → Whisper (transcribe as Hindi) → Translate to English
    """
    # Transcribe with Whisper
    transcript = transcribe_chunk_whisper(chunk_path)
    
    # If Hindi/Hinglish, translate to English
    if language.lower() == "hinglish":
        print(f"  → Translating Hindi to English...")
        transcript = translate_to_english(transcript, source_language="hi")
    
    return transcript


def transcribe_all(chunks: list, language: str = "english") -> str:
    """
    Transcribe all chunks using Whisper + optional translation.
    
    Args:
        chunks: List of audio file paths
        language: 'english' or 'hinglish'
    
    Returns:
        Full transcript as a single string
    """
    full_transcript = "" 
    engine = "Whisper + Translation" if language.lower() == "hinglish" else "Whisper"
    print(f"Using {engine} for transcription.")

    for i, chunk in enumerate(chunks):  
        print(f"Transcribing chunk {i + 1}/{len(chunks)}...")
        text = transcribe_chunk(chunk, language=language)  
        full_transcript += text + " "  

    print("Transcription complete.")
    return full_transcript.strip()  
