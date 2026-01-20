from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponse
from .models import Podcast
from .forms import ContactForm, PodcastUploadForm
from .transcribers_utils import transcribe_audio, segment_and_summarize
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

def index(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(request, "Message sent successfully!")
            return redirect('index')
    else:
        form = ContactForm()
    return render(request, 'transcriber/index.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'transcriber/register.html', {'form': form})

@login_required
def dashboard(request):
    podcasts = Podcast.objects.filter(user=request.user)
    return render(request, 'transcriber/dashboard.html', {'podcasts': podcasts})

@login_required
def upload_podcast(request):
    if request.method == 'POST':
        form = PodcastUploadForm(request.POST, request.FILES)
        if form.is_valid():
            podcast = form.save(commit=False)
            podcast.user = request.user
            podcast.status = 'processing'
            podcast.save()
            
            # Run AI Pipeline
            result = transcribe_audio(podcast.audio_file.path)
            if result:
                podcast.transcript_raw = result['text']
                podcast.transcript_final = segment_and_summarize(result['text'])
                podcast.detected_language = result['language']
                podcast.status = 'completed'
            else:
                podcast.status = 'failed'
            podcast.save()
            return redirect('dashboard')
    else:
        form = PodcastUploadForm()
    return render(request, 'transcriber/upload.html', {'form': form})

@login_required
def transcript_detail(request, pk):
    podcast = get_object_or_404(Podcast, pk=pk, user=request.user)
    if request.method == 'POST':
        podcast.transcript_final = request.POST.get('transcript_final')
        podcast.save()
        messages.success(request, "Changes saved!")
        return redirect('dashboard')
    return render(request, 'transcriber/transcript_detail.html', {'podcast': podcast})

@login_required
def download_pdf(request, pk):
    podcast = get_object_or_404(Podcast, pk=pk, user=request.user)
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.drawString(100, 750, f"Transcript: {podcast.title}")
    p.showPage()
    p.save()
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')