import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todolist_project.settings')
django.setup()

from django.contrib.auth.models import User

print(f"Total users: {User.objects.count()}")
for u in User.objects.all():
    print(f"User: {u.username}, Email: {u.email}, Is Superuser: {u.is_superuser}")
