from django.db import models

class CustomUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=False)
    password = models.CharField(max_length=128)  # Store hashed password

    def __str__(self):
        return self.username


# models.py
from django.db import models

class UserLink(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    job_role = models.CharField(max_length=200)
    url = models.URLField()
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.job_role
