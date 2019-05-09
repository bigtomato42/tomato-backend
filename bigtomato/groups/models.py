from django.db import models
from django.contrib.auth.models import User




class Group(models.Model):
    name = models.CharField(max_length=256)
    users = models.ManyToManyField(User)



    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=256)
    group = models.ForeignKey(Group, null=False, on_delete=models.deletion.CASCADE, related_name='tasks')
    finished = models.BooleanField(default=False)

    def __str__(self):
        return self.name
