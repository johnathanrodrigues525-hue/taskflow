from django.db import models


class Projeto(models.Model):
    STATUS = [
        ('planejado', 'Planejado'),
        ('andamento', 'Em Andamento'),
        ('concluido', 'Concluído'),
    ]
    nome = models.CharField(max_length=120)
    descricao = models.TextField(blank=True)
    responsavel = models.CharField(max_length=100)
    data_inicio = models.DateField()
    data_fim = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='planejado')

    def __str__(self):
        return self.nome

    @property
    def total_tarefas(self):
        return self.tarefas.count()


class Tarefa(models.Model):
    PRIORIDADE = [
        ('baixa', 'Baixa'),
        ('media', 'Média'),
        ('alta', 'Alta'),
    ]
    STATUS = [
        ('pendente', 'Pendente'),
        ('executando', 'Em Execução'),
        ('concluida', 'Concluída'),
    ]
    titulo = models.CharField(max_length=150)
    descricao = models.TextField(blank=True)
    prioridade = models.CharField(max_length=10, choices=PRIORIDADE, default='media')
    status = models.CharField(max_length=15, choices=STATUS, default='pendente')
    prazo = models.DateField(null=True, blank=True)

    # 🔗 RELACIONAMENTO COM PROJETO
    projeto = models.ForeignKey(
        Projeto,
        on_delete=models.CASCADE,
        related_name='tarefas'
    )

    def __str__(self):
        return f'{self.titulo} — {self.projeto.nome}'