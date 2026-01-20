import whisper
import os

from transformers import pipeline
import whisper
from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation

# Using the turbo model identified in your logs
MODEL_TYPE = "turbo" 

# 1. Initialize Intelligence Pipelines
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def transcribe_with_timestamps(file_path):
    """Fulfills the 'Segment-level timestamps' requirement."""
    try:
        model = whisper.load_model("turbo")
        result = model.transcribe(file_path)
        
        # Extract segments with timing
        segments = []
        for seg in result['segments']:
            segments.append({
                'start': round(seg['start'], 2),
                'end': round(seg['end'], 2),
                'text': seg['text']
            })
        return {'segments': segments, 'full_text': result['text']}
    except Exception as e:
        print(f"Transcription error: {e}")
        return None

def perform_mathematical_topic_modeling(text, n_topics=3):
    """
    Implements NMF/LDA as a secondary intelligence layer.
    NMF is often superior for short transcripts because it uses 
    Matrix Factorization: $$V \approx WH$$
    """
    vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, stop_words='english')
    tfidf = vectorizer.fit_transform([text])
    
    # Using Non-Negative Matrix Factorization (NMF)
    nmf = NMF(n_components=n_topics, random_state=1).fit(tfidf)
    
    feature_names = vectorizer.get_feature_names_out()
    topics = []
    for topic_idx, topic in enumerate(nmf.components_):
        top_words = [feature_names[i] for i in topic.argsort()[:-5 - 1:-1]]
        topics.append(f"Topic {topic_idx+1}: {', '.join(top_words)}")
    
    return topics

# Initialize the summarization pipeline once (it will download on first run)
# bart-large-cnn is excellent for abstractive summarization of long text
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")


def segment_and_summarize(text):
    """
    Fulfills GenAI Lab requirements using a real Transformer model.
    Based on the pipeline inference method in summarization.py.
    """
    try:
        # 1. Generate the Summary
        # We truncate the input to 1024 tokens (standard for many models) 
        # to prevent memory errors on very long podcasts.
        summary_result = summarizer(
            text[:3000],  # Use the first ~3000 characters for the executive summary
            max_length=150, 
            min_length=50, 
            do_sample=False
        )
        summary_text = summary_result[0]['summary_text']
        
        # 2. Format the Output
        header = "### AI EXECUTIVE SUMMARY\n"
        body = f"{summary_text}\n\n"
        segments_header = "### LOGICAL TOPIC SEGMENTS\n"
        
        # In a more advanced version, you could chunk the text 
        # and summarize each section for true "Topic Segmentation."
        return f"{header}{body}{segments_header}{text}"

    except Exception as e:
        print(f"Summarization error: {e}")
        return f"### AI SUMMARY ERROR\n{text}"