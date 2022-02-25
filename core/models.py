from django.db import models
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.conf import settings
import threading
import os

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

def email_certificados(nome, email):
    email = EmailMessage(
        'Certificado do II SiNeMIDE',
        'Body goes here',
        settings.EMAIL_HOST_USER,
        [email],
        reply_to=[settings.EMAIL_HOST_USER],
    )

    arquivo = os.path.join(settings.BASE_DIR, 'core', 'static', 'certificados', f'{nome}.pdf')
    
    email.attach_file(arquivo)
    email.send()

def enviar_email_certificados(nome, email):
    thread = threading.Thread(target=email_certificados, args=(nome, email))
    thread.start()

class Palestrantes(models.Model):
    nome = models.CharField(max_length=255, blank=False, null=False)
    imagem = models.CharField(max_length=255, blank=False, null=False)
    descricao = models.TextField()

    def __str__(self):
        return self.nome

    class Meta():
        verbose_name = "Palestrante"
        verbose_name_plural = "Palestrantes"

class Minicursos(models.Model):    
    nome = models.CharField(max_length=255, blank=False, null=False)
    responsavel = models.CharField(max_length=255, blank=False, null=False, default='Não há')
    dias = models.CharField(max_length=255, blank=False, null=False)
    horarios = models.CharField(max_length=255, blank=False, null=False)
    total_vagas = models.IntegerField()
    vagas_disponiveis = models.IntegerField(default=0)
    observacoes = models.TextField(blank=True)

    def __str__(self):
        return self.nome

    class Meta():
        verbose_name = "Minicurso"
        verbose_name_plural = "Minicursos"

class Usuarios(models.Model):
    tipos = [('Estudante Graduação', 'Estudante Graduação'), ('Estudante de Pós-Gradução', 'Estudante de Pós-Gradução'), ('Docente', 'Docente'), ('Outros Profissionais', 'Outros Profissionais')]
    
    nome = models.CharField(max_length=255, blank=False, null=False)
    instituicao = models.CharField(max_length=255, blank=False, null=False)
    email = models.CharField(max_length=255, blank=False, null=False)
    cpf = models.CharField(max_length=255, blank=False, null=False)
    tipo_usuario = models.CharField(max_length=255, blank=False, null=False, choices=tipos)
    minicurso = models.ManyToManyField(Minicursos)

    def __str__(self):
        return self.nome

    class Meta():
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        enviar_email_registro(self)

class Emails(models.Model):
    assunto = models.CharField(max_length=255, blank=False, null=False)
    mensagem = models.TextField(blank=False, null=False)

    def __str__(self):
        return self.assunto

    class Meta():
        verbose_name = "E-mail"
        verbose_name_plural = "E-mails"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        destinatarios = Usuarios.objects.values_list('email', flat=True)

        destinatarios_1 = destinatarios[:400]
        destinatarios_2 = destinatarios[400:]

        print(destinatarios, destinatarios_1, destinatarios_2)

        enviar_email(assunto=self.assunto, mensagem=self.mensagem, destinatarios=destinatarios_1)
        enviar_email(assunto=self.assunto, mensagem=self.mensagem, destinatarios=destinatarios_2)

class Ajustes(models.Model):
    inscricoes_ativas = models.BooleanField(default=True)

    class Meta():
        verbose_name = "Ajuste"
        verbose_name_plural = "Ajustes"