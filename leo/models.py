from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    text = models.CharField(max_length=500)
    emotions = models.CharField(max_length=700)
    before = models.CharField(max_length=100)
    after = models.CharField(max_length=100)

    def __str__(self):
        return self.name
