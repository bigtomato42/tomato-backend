from django.db import models
from django.contrib.auth.models import User
from django.db import transaction

class Group(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=256, null=True)

    users = models.ManyToManyField(User, related_name='group_set')

    owner = models.ForeignKey(User, on_delete=models.deletion.CASCADE, related_name='group_owner')

    pending_invitations = models.ManyToManyField(User, related_name='invited_to_groups')

    def __str__(self):
        return self.name

    def accepted_invitation(self, user):
        with transaction.atomic():
            self.pending_invitations.remove(user)
            self.users.add(user)


class Task(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=256)
    group = models.ForeignKey(Group, null=False, on_delete=models.deletion.CASCADE, related_name='tasks')
    finished = models.BooleanField(default=False)

    def __str__(self):
        return self.name
