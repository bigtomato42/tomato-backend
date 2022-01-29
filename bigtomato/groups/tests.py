from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase
from django.urls import reverse

from bigtomato.groups.models import Group


class SetUpUsersMixin(object):
    def setUp(self):
        # set up three users
        user1 = {"username": "user1", "password": "test_password", "email": "test@test.com"}
        user2 = {"username": "user2", "password": "test_password", "email": "test@test.com"}
        user3 = {"username": "user3", "password": "test_password", "email": "test@test.com"}

        u1 = User.objects.create_user(**user1)
        u2 = User.objects.create_user(**user2)
        u3 = User.objects.create_user(**user3)

        # user2 owns a group, invites user1
        group = Group.objects.create(pk=144, name="group_test", owner=u2)
        group.users.add(u2)
        group.pending_invitations.add(u1)


class TestGroup(SetUpUsersMixin, TestCase):
    def test_accepted_invitation(self):
        group = Group.objects.get(name="group_test")
        user1 = User.objects.get(username="user1")

        group.accept_invitation(user1)

        assert user1 not in group.pending_invitations.all(), "user is still in pending invitations"
        assert user1 in group.users.all(), "user did not become a member of a group"

    def test_cannot_accept_invitation(self):
        group = Group.objects.get(name="group_test")
        user3 = User.objects.get(username="user3")

        group.accept_invitation(user3)

        assert user3 not in group.users.all(), "user did become member of a group when he was not invited"


class TestGroupEndpoints(SetUpUsersMixin, TestCase):
    def test_create_group_endpoint_success(self):
        params = {"name": "test_group455", "description": "best_group"}
        user = User.objects.get(username="user1")
        self.client.force_login(user)
        response = self.client.post("/groups/", params)

        assert response.status_code == 201
        assert Group.objects.filter(name="test_group455").count() > 0, "Create group endpoint should create a group"
        new_group = Group.objects.get(name="test_group455")
        assert user == new_group.owner and user in new_group.users.all()

    def test_create_group_endpoint_fail(self):
        user = User.objects.get(username="user1")
        self.client.force_login(user)
        response = self.client.post("/groups/", {})
        assert response != 201, "New group was created even when no name parameter was supplied"

    # def test_group_detail_success(self):
    #     print(User.objects.all())
    #     user = User.objects.get(username='user2')
    #     group_pk = Group.objects.get(name='group_test').pk
    #     self.client.force_login(user)
    #     response = self.client.get('/groups/{0}/'.format(group_pk))
    #     print(response.__dict__)
    #     assert response == 200, 'Group detail endpoint should work'
    #
    # def test_group_detail_fail(self):
    #     user = User.objects.get(username='user1')
    #     self.client.force_login(user)
    #     response = self.client.get('/groups/144/')
    #     assert response == 404, 'Group detail endpoint should not work for a user who is not in group'
    #
    # def test_group_list_success(self):
    #     pass
    #
    # def test_group_invite_users_success(self):
    #     pass
    #
    # def test_group_pending_invitation_success(self):
    #     pass
    #
    # def test_group_accept_invitation_success(self):
    #     pass
