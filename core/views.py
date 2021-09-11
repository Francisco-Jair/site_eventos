from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import csrf_protect
from .models import Palestrantes, Minicursos, Usuarios

def index(request):
    palestrantes = Palestrantes.objects.all()
    minicursos = Minicursos.objects.exclude(vagas_disponiveis__lte=0)
    dados = {'palestrantes': palestrantes, 'minicursos': minicursos}
    return render(request, 'index.html', dados)

def detalhes_palestrante(request):
    try:
        palestrante = Palestrantes.objects.filter(imagem=request.GET.get('palestrante')).first()
        dados = {'palestrante': palestrante}
        return render(request, 'speaker-details.html', dados)
    except:
        return redirect('')

@csrf_protect
def inscricao(request):

    try:
        if request.method == 'POST':
            palestrantes = Palestrantes.objects.all()
            minicursos = Minicursos.objects.exclude(vagas_disponiveis=0)
            
            usuario = Usuarios.objects.create(nome = request.POST['nome'], 
                instituicao = request.POST['instituicao'], 
                email = request.POST['email'],
                cpf = request.POST['cpf'], 
                tipo_usuario = request.POST['tipo-usuario'])
    
            for curso in dict(request.POST)['cursos']:
                c = Minicursos.objects.get(nome=curso)
                usuario.minicurso.add(Minicursos.objects.get(nome=curso))
                if(c.vagas_disponiveis > 0):
                    c.vagas_disponiveis -= 1
                    c.save()
                else:
                    raise Exception

            usuario.save()
            dados = {'palestrantes': palestrantes, 'minicursos': minicursos, 'mensagem': 'Inscrição cadastrada com sucesso.'}
            return render(request, 'index.html', dados)

    except KeyError:
        dados = {'palestrantes': palestrantes, 'minicursos': minicursos, 'mensagem': 'Inscrição cadastrada com sucesso.'}
        return render(request, 'index.html', dados)
    except:
        dados = {'palestrantes': palestrantes, 'minicursos': minicursos, 'mensagem': 'Não foi possível concluir sua inscrição. Por favor, tente novamente.'}
        return render(request, 'index.html', dados)

