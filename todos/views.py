from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Task
from django.contrib.auth.models import User
from .forms import SignUpForm

# --- Public/Auth Views ---

def signup(request):
    """
    Handle user registration.
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Auto-login after signup
            return redirect('task_list')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

# --- Task Views (Protected) ---

@login_required
def task_list(request):
    """
    Display tasks belonging to the logged-in user.
    """
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'todos/task_list.html', {'tasks': tasks})

@login_required
def task_create(request):
    """
    Create a new task for the logged-in user.
    """
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        
        if title:
            Task.objects.create(
                user=request.user, # Assign current user
                title=title, 
                description=description,
                due_date=due_date if due_date else None
            )
            return redirect('task_list')
    
    return render(request, 'todos/task_form.html')

@login_required
def task_update(request, pk):
    """
    Update a task (ensure it belongs to the user).
    """
    task = get_object_or_404(Task, pk=pk, user=request.user) # Security: filter by user
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        due_date_str = request.POST.get('due_date')
        task.due_date = due_date_str if due_date_str else None
        task.completed = 'completed' in request.POST
        task.save()
        return redirect('task_list')
    
    return render(request, 'todos/task_form.html', {'task': task})

@login_required
def task_delete(request, pk):
    """
    Delete a task (ensure it belongs to the user).
    """
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    
    return render(request, 'todos/task_confirm_delete.html', {'task': task})

@login_required
def task_toggle_complete(request, pk):
    """
    Toggle completion status.
    """
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.completed = not task.completed
    task.save()
    return redirect('task_list')

# --- Admin Dashboard (Superuser Only) ---

@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    """
    Custom dashboard for superusers to view all users.
    """
    users = User.objects.all().order_by('-date_joined')
    user_stats = []
    for u in users:
        user_stats.append({
            'user': u,
            'task_count': Task.objects.filter(user=u).count()
        })
        
    return render(request, 'todos/admin_dashboard.html', {'user_stats': user_stats})

@user_passes_test(lambda u: u.is_superuser)
def admin_delete_user(request, user_id):
    """
    Allow superuser to delete a user account.
    """
    user_to_delete = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        # Prevent self-deletion if you want, but standard is allowed usually. 
        # Let's add simple check to avoid accidental lockout if they only have one admin
        if user_to_delete == request.user:
            # For now, let's just allow it or maybe redirect with error. 
            # But simpler to just proceed.
            pass
        user_to_delete.delete()
        return redirect('admin_dashboard')
    
    # We can reuse the confirm delete or create a specific one.
    # For speed, let's just do a simple confirm page or reuse.
    return render(request, 'todos/admin_confirm_user_delete.html', {'user_to_delete': user_to_delete})
