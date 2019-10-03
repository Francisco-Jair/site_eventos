from django.shortcuts import render

def index(request):
    dados = {}

    return render(request, 'index.html', dados)

def speaker_details(request):
    dados = {}

    return render(request, 'speaker-details.html', dados)
