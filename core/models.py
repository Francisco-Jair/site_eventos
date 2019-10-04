from django.db import models

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