from apps.abstract.models import AbstractCommon
from django.db import models


class Student(AbstractCommon):
    """Model for Student"""
    name = models.CharField("Nome do aluno", max_length=150)
    email = models.EmailField("Email", unique=True)
    birthday = models.DateField("Data de aniversário")

    class Meta:
        verbose_name = 'Aluno'

    def __str__(self):
        return self.name
