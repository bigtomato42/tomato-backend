from django.db import models
from django.contrib.auth.models import User
from django.db import transaction


class GroupManager(models.Manager):

    def create_group(self, owner, kwargs):
        group = Group.objects.create(owner=owner, **kwargs)
        group.users.add(owner)
        return group


class Group(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=256, null=True, blank=True)

    users = models.ManyToManyField(User, related_name='group_set')

    owner = models.ForeignKey(User, on_delete=models.deletion.CASCADE, related_name='group_owner')

    pending_invitations = models.ManyToManyField(User, related_name='invited_to_groups')

    objects = GroupManager()

    def __str__(self):
        return self.name

    @transaction.atomic
    def accept_invitation(self, user):
        if user in self.pending_invitations.all():
            self.pending_invitations.remove(user)
            self.users.add(user)
