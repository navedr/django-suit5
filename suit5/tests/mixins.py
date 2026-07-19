from django.contrib.auth.models import User
from django.test import TestCase
from random import randint
from django.urls import reverse


class UserTestCaseMixin(TestCase):
    superuser = None
    user = None

    def login_superuser(self):
        if not self.superuser:
            self.superuser = self.create_superuser()
        self.client.login(username=self.superuser.username, password='password')

    def create_superuser(self):
        return User.objects.create_superuser('admin-%s' % str(randint(1, 9999)),
                                             'test@test.com', 'password')

    def create_user(self):
        user = User.objects.create_user('user-%s' % str(randint(1, 9999)),
                                        'test2@test2.com', 'password')
        user.is_staff = True
        user.save()
        return user

    def login_user(self):
        if not self.user:
            self.user = self.create_user()
        self.client.login(username=self.user.username, password='password')

    def get_response(self, url=None):
        url = url or reverse('admin:index')
        self.response = self.client.get(url)


class ModelsTestCaseMixin:
    pass
