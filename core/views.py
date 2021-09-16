from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from .models import Palestrantes, Minicursos, Usuarios
from django.core.mail import send_mail
from django.conf import settings
import threading

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
            
            usuario = Usuarios.objects.create(
                nome = request.POST['nome'], 
                instituicao = request.POST['instituicao'], 
                email = request.POST['email'],
                cpf = request.POST['cpf'], 
                tipo_usuario = request.POST['tipo-usuario']
            )

            usuario.save()

            enviar_email_registro(usuario)
            
            dados = {'palestrantes': palestrantes, 'minicursos': minicursos, 'mensagem': 'Inscrição cadastrada com sucesso.'}

            return render(request, 'index.html', dados)

    except KeyError:
        dados = {'palestrantes': palestrantes, 'minicursos': minicursos, 'mensagem': 'Inscrição cadastrada com sucesso.'}

        return render(request, 'index.html', dados)
    except:
        dados = {'palestrantes': palestrantes, 'minicursos': minicursos, 'mensagem': 'Não foi possível concluir sua inscrição. Por favor, tente novamente.'}

        return render(request, 'index.html', dados)

def email(assunto, mensagem, remetente, destinatarios):
    send_mail(assunto, mensagem, remetente, destinatarios)

def enviar_email(assunto='', mensagem='', remetente=settings.EMAIL_HOST_USER, destinatarios=[]):
    thread = threading.Thread(target=email, args=(assunto, mensagem, remetente, destinatarios))
    thread.start()

def enviar_email_registro(usuario):
    assunto = 'Inscrição confirmada!'
    mensagem = f'Olá, {usuario.nome},\n\nParabéns, sua inscrição no II Simpósio Nordestino de Mídias Digitais para a Educação – SiNeMIDE foi confirmada com sucesso.\n\nLembrando que o SiNeMIDE ocorrerá nos dias nos dias 23 e 24 de setembro de 2021.\n\nPara obter mais informações e a nossa programação completa, acesse nosso site: https://bit.ly/2VI72QS.'
    destinatarios = [usuario.email]

    enviar_email(assunto=assunto, mensagem=mensagem, destinatarios=destinatarios)

def handler404(request, exception):
    response = render(request, '404.html', {})
    response.status_code = 404
    
    return response
