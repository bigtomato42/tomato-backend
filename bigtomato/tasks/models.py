from django.db import models

from bigtomato.groups.models import Group


class Task(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=256)
    group = models.ForeignKey(Group, null=False, on_delete=models.deletion.CASCADE, related_name="tasks")
    finished = models.BooleanField(default=False)

    def __str__(self):
        return self.name
