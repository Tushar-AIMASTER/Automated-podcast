import whisper
from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation, TruncatedSVD

# Using the pipeline method for abstractive summarization
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def transcribe_audio(file_path):
    try:
        model = whisper.load_model("turbo")
        result = model.transcribe(file_path)
        # Format segments for the Timeline UI
        formatted_segments = []
        for s in result['segments']:
            formatted_segments.append(f"[{int(s['start'])}s] {s['text'].strip()}")
            
        return {
            'text': result['text'],
            'language': result.get('language', 'en'),
            'segments_list': formatted_segments # Helper for storage
        }
    except Exception as e:
        print(f"ASR Error: {e}")
        return None

def segment_and_summarize(text):
    """Integrates LLM Summary and Math Topic Modeling."""
    if not text: return ""

    # 1. LLM Abstractive Summary
    try:
        summary = summarizer(text[:3000], max_length=130, min_length=30, do_sample=False)[0]['summary_text']
    except: summary = "Summary generation failed."

    # 2. Topic Modeling (NMF, LDA, LSA)
    topics = _run_all_topic_models(text)

    # 3. Combine into a structured string using specific markers for the View to parse
    return f"[[SUMMARY]]\n{summary}\n\n[[TOPICS]]\n{topics}\n\n[[CONTENT]]\n{text}"

def _run_all_topic_models(text):
    """Runs NMF, LDA, and LSA Topic Modeling."""
    try:
        tfidf_vect = TfidfVectorizer(stop_words='english')
        tfidf = tfidf_vect.fit_transform([text])
        words = tfidf_vect.get_feature_names_out()

        # NMF - Non-Negative Matrix Factorization
        nmf = NMF(n_components=1, random_state=1).fit(tfidf)
        nmf_words = [words[i] for i in nmf.components_[0].argsort()[-3:]]

        # LSA - Latent Semantic Analysis (Truncated SVD)
        lsa = TruncatedSVD(n_components=1, random_state=1).fit(tfidf)
        lsa_words = [words[i] for i in lsa.components_[0].argsort()[-3:]]

        return f"NMF: {', '.join(nmf_words)} | LSA: {', '.join(lsa_words)}"
    except: return "No topics detected."