from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from todos.models import Task
from datetime import timedelta

class Command(BaseCommand):
    help = 'Send email reminders for tasks due within the next hour'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        one_hour_from_now = now + timedelta(hours=1)
        
        # Find tasks that:
        # 1. Have a due date
        # 2. Are not completed
        # 3. Reminder has not been sent yet
        # 4. Due date is within the next hour (and in the future)
        tasks = Task.objects.filter(
            due_date__range=(now, one_hour_from_now),
            completed=False,
            reminder_sent=False
        )

        if not tasks.exists():
            self.stdout.write(self.style.SUCCESS('No tasks due in the next hour.'))
            return

        for task in tasks:
            if task.user and task.user.email:
                subject = f'Reminder: Task "{task.title}" is due soon!'
                message = f'Hi {task.user.username},\n\nThis is a reminder that your task "{task.title}" is due at {task.due_date.strftime("%Y-%m-%d %H:%M")}.\n\nPlease ensure it is completed on time.\n\nBest regards,\nToDo List Team'
                
                try:
                    send_mail(
                        subject,
                        message,
                        'webmaster@localhost',
                        [task.user.email],
                        fail_silently=False,
                    )
                    task.reminder_sent = True
                    task.save()
                    self.stdout.write(self.style.SUCCESS(f'Sent reminder for task "{task.title}" to {task.user.email}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Failed to send email to {task.user.email}: {e}'))
            else:
                 self.stdout.write(self.style.WARNING(f'Task "{task.title}" has no user or user has no email.'))
