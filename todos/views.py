from django.shortcuts import render, redirect, get_object_or_404
from .models import Task

def task_list(request):
    """
    View to display the list of all tasks.
    """
    tasks = Task.objects.all()
    return render(request, 'todos/task_list.html', {'tasks': tasks})

def task_create(request):
    """
    View to create a new task.
    Handle both GET (show form) and POST (save task) requests.
    """
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date') # Keep as string, let DB handle parse or validation layer if expanded
        
        # Basic validation handled by frontend or model save for now
        if title:
            Task.objects.create(
                title=title, 
                description=description,
                due_date=due_date if due_date else None
            )
            return redirect('task_list')
    
    return render(request, 'todos/task_form.html') # Reusing or separate template for create? Let's use list or modal usually, but for simple request let's do a page.

def task_update(request, pk):
    """
    View to update an existing task.
    """
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        due_date_str = request.POST.get('due_date')
        task.due_date = due_date_str if due_date_str else None
        task.completed = 'completed' in request.POST
        task.save()
        return redirect('task_list')
    
    return render(request, 'todos/task_form.html', {'task': task})

def task_delete(request, pk):
    """
    View to delete a task.
    """
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    
    return render(request, 'todos/task_confirm_delete.html', {'task': task})

def task_toggle_complete(request, pk):
    """
    Quick toggle for completion status from the list view.
    """
    task = get_object_or_404(Task, pk=pk)
    task.completed = not task.completed
    task.save()
    return redirect('task_list')
