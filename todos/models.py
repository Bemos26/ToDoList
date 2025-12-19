from django.db import models

class Task(models.Model):
    """
    Model representing a task in the ToDo list.
    """
    # Title of the task, limited to 200 characters
    title = models.CharField(max_length=200)
    
    # Optional detailed description of the task
    description = models.TextField(blank=True, null=True)
    
    # Status of the task: True if completed, False otherwise
    completed = models.BooleanField(default=False)
    
    # Link to the user who owns this task
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    
    # Timestamp when the task was created
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Optional due date for the task
    due_date = models.DateTimeField(blank=True, null=True)
    
    # Track if reminder email has been sent
    reminder_sent = models.BooleanField(default=False)

    def __str__(self):
        """
        String representation of the Task model, returning the title.
        """
        return self.title

    class Meta:
        # Sort tasks by creation date (newest first) by default
        ordering = ['-created_at']
