from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from .models import Ajustes, Palestrantes, Minicursos, Usuarios

def index(request):
    palestrantes = Palestrantes.objects.all()
    minicursos = Minicursos.objects.exclude(vagas_disponiveis__lte=0)
    ajustes = Ajustes.objects.first()

    dados = {'palestrantes': palestrantes, 'minicursos': minicursos, 'ajustes': ajustes}

    return render(request, 'index.html', dados)

def detalhes_palestrante(request):
    try:
        palestrante = Palestrantes.objects.filter(imagem=request.GET.get('palestrante')).first()
        ajustes = Ajustes.objects.first()

        dados = {'palestrante': palestrante, 'ajustes': ajustes}

        return render(request, 'speaker-details.html', dados)
    except:
        return redirect('')

@csrf_protect
def inscricao(request):
    ajustes = Ajustes.objects.first()

    try:
        if request.method == 'POST':
            palestrantes = Palestrantes.objects.all()
            minicursos = Minicursos.objects.exclude(vagas_disponiveis=0)
            
            usuario = Usuarios.objects.create(
                nome = request.POST['nome'], 
                instituicao = request.POST['instituicao'], 
                email = request.POST['email'],
                cpf = request.POST['cpf'], 
                tipo_usuario = request.POST['tipo-usuario']
            )

            usuario.save()
            
            dados = {'palestrantes': palestrantes, 'minicursos': minicursos, 'mensagem': 'Inscrição cadastrada com sucesso.', 'ajustes': ajustes}

            return render(request, 'index.html', dados)

    except KeyError:
        dados = {'palestrantes': palestrantes, 'minicursos': minicursos, 'mensagem': 'Inscrição cadastrada com sucesso.', 'ajustes': ajustes}

        return render(request, 'index.html', dados)
    except:
        dados = {'palestrantes': palestrantes, 'minicursos': minicursos, 'mensagem': 'Não foi possível concluir sua inscrição. Por favor, tente novamente.', 'ajustes': ajustes}

        return render(request, 'index.html', dados)

def handler404(request, exception):
    response = render(request, '404.html', {})
    response.status_code = 404
    
    return response
