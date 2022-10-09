import json
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

    __discipline_id = None
    __discipline = {
        'name': 'temporary discipline',
        'workload': '20',
    }

    __student_id = None
    __student = {
        'name': 'temporary',
        'email': 'temporary@temporary.com',
        'birthday': '2022-10-07'
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

        response = self.client.post('/api/v1/disciplina/', self.get_discipline())
        self.assertEqual(response.status_code, 201)
        self.set_discipline_id(json.loads(response.content)['disciplina']['id'])

        response = self.client.post('/api/v1/aluno/', self.get_student())
        self.assertEqual(response.status_code, 201)
        self.set_student_id(json.loads(response.content)['aluno']['id'])

    def get_user(self):
        """Get User"""
        return self.__user

    def get_discipline(self):
        """Get Discipline"""
        return self.__discipline

    def get_discipline_id(self):
        """Get Discipline id"""
        return self.__discipline_id

    def get_student(self):
        """Get Student"""
        return self.__student

    def get_student_id(self):
        """Get Student id"""
        return self.__student_id

    def set_student(self, field, value):
        """Update field in Student, return Student"""
        self.__student[field] = value
        return self.__student

    def set_user(self, field, value):
        """Update field in User, return User"""
        self.__user[field] = value
        return self.__user

    def set_discipline(self, field, value):
        """Update field in Discipline, return Discipline"""
        self.__discipline[field] = value
        return self.__discipline

    def set_discipline_id(self, value):
        """Update discipline id"""
        self.__discipline_id = value

    def set_student_id(self, value):
        """Update student id"""
        self.__student_id = value

    def printl(self, msg):
        """Print in time execution"""
        self.stdout = OutputWrapper(sys.stdout)
        self.stderr = OutputWrapper(sys.stderr)
        self.style = color_style()
        self.stdout.write(self.style.SUCCESS(msg))
