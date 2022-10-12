from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    '''
    models.CASCADE means the user is deleted, the item will also be deleted.
    models.SET_NULL means the user is deleted, the item remains.
    null = True means when submit to database, it is allowed to be empty
    blank = True means when submitting the form, it is allowed to be blank
    '''
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete']
