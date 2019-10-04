from django.shortcuts import render, redirect
from .models import Palestrantes, Minicursos

def index(request):
    palestrantes = Palestrantes.objects.all()
    minicursos = Minicursos.objects.exclude(vagas_disponiveis = 0)

    dados = {'palestrantes': palestrantes, 'minicursos': minicursos}

    return render(request, 'index.html', dados)

def detalhes_palestrante(request):
    try:
        palestrante = Palestrantes.objects.filter(imagem=request.GET.get('palestrante')).first()
        dados = {'palestrante': palestrante}

        print(dados)

        return render(request, 'speaker-details.html', dados)
    except:
        return redirect('')

# def inscricao(request):
    # if request.method == 'POST':

