# transcriber/transcribers_utils.py
import whisper
import os

# Load model once to save resources (or load inside function if RAM is tight)
# Using "turbo" as requested in your file, or "base" for speed
MODEL_TYPE = "turbo" 

def transcribe_audio(file_path):
    """
    Transcribes full audio file using OpenAI Whisper.
    Returns dictionary with text and language.
    """
    try:
        model = whisper.load_model(MODEL_TYPE)
        
        # Standard transcription for full files (handles chunks automatically)
        result = model.transcribe(file_path)
        
        return {
            'text': result['text'],
            'language': result.get('language', 'unknown')
        }
    except Exception as e:
        print(f"Error in transcription: {e}")
        return None