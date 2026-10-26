from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .forms import TaskForm
from .models import Task


def task_list(request):
    status = request.GET.get('status', 'all')
    tasks = Task.objects.all()

    if status == 'pending':
        tasks = tasks.filter(completed=False)
    elif status == 'completed':
        tasks = tasks.filter(completed=True)

    total = Task.objects.count()
    done = Task.objects.filter(completed=True).count()

    context = {
        'tasks': tasks,
        'status': status,
        'total': total,
        'done': done,
        'pending': total - done,
        'percent': int(done / total * 100) if total else 0,
    }
    return render(request, 'tasks/task_list.html', context)


def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task added successfully!')
            return redirect('tasks:list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form, 'title': 'Add Task'})


def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated!')
            return redirect('tasks:list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form, 'title': 'Edit Task'})


def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        messages.warning(request, 'Task deleted.')
        return redirect('tasks:list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})


@require_POST
def task_toggle(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.completed = not task.completed
    task.save()
    return redirect('tasks:list')