from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    text = models.CharField(max_length=500)

    def __str__(self):
        return self.name
