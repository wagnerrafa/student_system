import sys

from django.core.management import color_style
from django.core.management.base import OutputWrapper
from django.test import TestCase


class AbstractTest(TestCase):
    """Add common methods to all testcase"""

    __user = {'username': 'temporary',
              'email': 'temporary@gmail.com',
              'first_name': 'temporary',
              'last_name': 'temporary',
              'password': 'temporary_passwd1',
              'password_confirm': 'temporary_passwd1',
              }

    def setUp(self):
        """Create User for api requests that need authentication"""
        user = {'username': 'temporary',
                'email': 'temporary@gmail.com',
                'first_name': 'temporary',
                'last_name': 'temporary',
                'birthday': '2022-10-06',
                'password': 'temporary_passwd1',
                'password_confirm': 'temporary_passwd1',
                }
        response = self.client.post('/api/v1/user/', user)
        self.assertEqual(response.status_code, 201)

    def get_user(self):
        """Get User"""
        return self.__user

    def set_user(self, field, value):
        """Update field in User, return User"""
        self.__user[field] = value
        return self.__user

    def printl(self, msg):
        """Print in time execution"""
        self.stdout = OutputWrapper(sys.stdout)
        self.stderr = OutputWrapper(sys.stderr)
        self.style = color_style()
        self.stdout.write(self.style.SUCCESS(msg))
