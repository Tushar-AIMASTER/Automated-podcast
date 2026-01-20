
---

# AutoScript AI: Automated Podcast Intelligence

AutoScript AI is an end-to-end web platform designed to transform raw podcast audio into structured, actionable intelligence. It leverages state-of-the-art Generative AI and Machine Learning models to provide high-fidelity transcriptions, executive summaries, and mathematical thematic analysis.

## 🚀 Key Features

* **High-Fidelity Transcription**: Utilizes OpenAI's **Whisper Turbo** model for rapid and accurate speech-to-text conversion with built-in timestamp generation.
* **Abstractive Summarization**: Implements the **BART (Large-CNN)** model via Hugging Face Transformers to generate concise, human-like executive summaries.
* **Thematic Pattern Discovery**: Employs mathematical modeling techniques, including **NMF (Non-negative Matrix Factorization)**, **LSA (Latent Semantic Analysis)**, and **LDA (Latent Dirichlet Allocation)**, to identify core topics within the audio.
* **Structured Timeline**: Automatically segments transcripts into chronological paragraphs with associated timestamps for easy navigation.
* **PDF Export**: Allows for professional verification and one-click export of transcripts and AI insights to PDF format.

## 🛠️ System Architecture & Flow

1. **Ingestion**: Secure upload of raw podcast audio in MP3 or WAV formats.
2. **ASR Engine**: Full-stream processing using Whisper Turbo to produce text segments.
3. **Logic Layer**: A multi-stage GenAI pipeline that handles abstractive summarization and topic segmentation.
4. **Verification**: A dedicated review interface where users can manually edit and verify AI-generated content.
5. **Responsibility**: Integration of safety filters and confidence-based fallbacks to ensure content reliability.

## 📦 Prerequisites

* Python 3.9+
* Django 4.x
* FFmpeg (required for audio processing)
* Virtual Environment (recommended)

## 🔧 Installation & Setup

1. **Clone the Repository**
```bash
git clone https://github.com/Tushar-AIMASTER/Automated-podcast/tree/main/Intern_Submissions/TUSHAR_SRIVASTAVA/Automated_Transcript_generation.git
cd Automated_Transcript_generation

```


2. **Create a Virtual Environment**
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

```


3. **Install Dependencies**
```bash
pip install django torch transformers openai-whisper scikit-learn numpy

```


4. **Initialize Database**
```bash
python manage.py makemigrations
python manage.py migrate

```


5. **Launch Server**
```bash
python manage.py runserver

```



## 🖥️ Project Structure

* `base.html`: The master template featuring a modern, responsive navigation system and light-themed aesthetic.
* `index.html`: Product landing page showcasing system architecture and GenAI capabilities.
* `transcript_detail.html`: The core AI review interface, displaying the timeline transcript, executive summary, and topic tags side-by-side.
* `dashboard.html`: User management portal for tracking the status of processed podcasts.

Automated_Transcript_generation/           <-- (Project Root Folder)
│
├── manage.py                              <-- (Django Management Script)
├── db.sqlite3                             <-- (Database - created after migrate)
│
├── media/                                 <-- (Stores Uploaded Audio)
│   └── podcasts/                          <-- (Files saved here)
│
├── Automated_Transcript_generation/       <-- (Configuration Folder)
│   ├── __init__.py
│   ├── settings.py                        <-- (Added MEDIA/LOGIN settings)
│   ├── urls.py                            <-- (Main URL config)
│   └── wsgi.py
│
└── transcriber/                           <-- (Main Application App)
    ├── __init__.py
    ├── admin.py                           <-- (Admin Panel config)
    ├── apps.py
    ├── forms.py                           <-- (Contact, Upload, Edit forms)
    ├── models.py                          <-- (Podcast model)
    ├── transcribers_utils.py              <-- (Whisper AI Logic)
    ├── urls.py                            <-- (App specific routes)
    ├── views.py                           <-- (Logic for all pages)
    │
    ├── migrations/                        <-- (Database migration tracking)
    │   └── __init__.py
    │
    └── templates/                         <-- (All HTML files)
        ├── registration/                  <-- (CRITICAL: For Auth system)
        │   └── login.html                 <-- (The login page)
        │
        └── transcriber/                   <-- (Application Templates)
            ├── base.html                  <-- (Navbar & Layout)
            ├── index.html                 <-- (Landing Page)
            ├── dashboard.html             <-- (User Dashboard)
            ├── upload.html                <-- (File Upload page)
            ├── transcript_detail.html     <-- (Review/Edit Transcript)
            └── register.html              <-- (Signup page)