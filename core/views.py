from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Projeto, Tarefa


# ---------- HOME ----------
def home(request):
    return render(request, 'core/home.html', {
        'total_projetos': Projeto.objects.count(),
        'total_tarefas': Tarefa.objects.count(),
        'pendentes': Tarefa.objects.filter(status='pendente').count(),
    })


# ---------- PROJETO ----------
def lista_projetos(request):
    return render(request, 'core/projeto/lista.html',
                  {'projetos': Projeto.objects.all()})


def criar_projeto(request):
    if request.method == 'POST':
        Projeto.objects.create(
            nome=request.POST['nome'],
            descricao=request.POST.get('descricao', ''),
            responsavel=request.POST['responsavel'],
            data_inicio=request.POST['data_inicio'],
            data_fim=request.POST.get('data_fim') or None,
            status=request.POST.get('status', 'planejado'),
        )
        messages.success(request, 'Projeto criado com sucesso!')
        return redirect('lista_projetos')
    return render(request, 'core/projeto/form.html')


def editar_projeto(request, id):
    p = get_object_or_404(Projeto, id=id)
    if request.method == 'POST':
        p.nome = request.POST['nome']
        p.descricao = request.POST.get('descricao', '')
        p.responsavel = request.POST['responsavel']
        p.data_inicio = request.POST['data_inicio']
        p.data_fim = request.POST.get('data_fim') or None
        p.status = request.POST.get('status')
        p.save()
        messages.success(request, 'Projeto atualizado!')
        return redirect('lista_projetos')
    return render(request, 'core/projeto/form.html', {'projeto': p})


def excluir_projeto(request, id):
    p = get_object_or_404(Projeto, id=id)
    if request.method == 'POST':
        p.delete()
        messages.success(request, 'Projeto excluído.')
        return redirect('lista_projetos')
    return render(request, 'core/projeto/confirmar_exclusao.html', {'projeto': p})


def detalhe_projeto(request, id):
    p = get_object_or_404(Projeto, id=id)
    return render(request, 'core/projeto/detalhe.html',
                  {'projeto': p, 'tarefas': p.tarefas.all()})


# ---------- TAREFA ----------
def lista_tarefas(request):
    qs = Tarefa.objects.select_related('projeto').all()
    filtro = request.GET.get('projeto')
    if filtro:
        qs = qs.filter(projeto_id=filtro)
    return render(request, 'core/tarefa/lista.html',
                  {'tarefas': qs,
                   'projetos': Projeto.objects.all(),
                   'projeto_filtro': filtro})


def criar_tarefa(request):
    projetos = Projeto.objects.all()
    if request.method == 'POST':
        Tarefa.objects.create(
            titulo=request.POST['titulo'],
            descricao=request.POST.get('descricao', ''),
            prioridade=request.POST.get('prioridade', 'media'),
            status=request.POST.get('status', 'pendente'),
            prazo=request.POST.get('prazo') or None,
            projeto=get_object_or_404(Projeto, id=request.POST['projeto']),
        )
        messages.success(request, 'Tarefa criada!')
        return redirect('lista_tarefas')
    return render(request, 'core/tarefa/form.html', {'projetos': projetos})


def editar_tarefa(request, id):
    t = get_object_or_404(Tarefa, id=id)
    if request.method == 'POST':
        t.titulo = request.POST['titulo']
        t.descricao = request.POST.get('descricao', '')
        t.prioridade = request.POST.get('prioridade')
        t.status = request.POST.get('status')
        t.prazo = request.POST.get('prazo') or None
        t.projeto = get_object_or_404(Projeto, id=request.POST['projeto'])
        t.save()
        messages.success(request, 'Tarefa atualizada!')
        return redirect('lista_tarefas')
    return render(request, 'core/tarefa/form.html',
                  {'tarefa': t, 'projetos': Projeto.objects.all()})


def excluir_tarefa(request, id):
    t = get_object_or_404(Tarefa, id=id)
    if request.method == 'POST':
        t.delete()
        messages.success(request, 'Tarefa excluída.')
        return redirect('lista_tarefas')
    return render(request, 'core/tarefa/confirmar_exclusao.html', {'tarefa': t})