from django.db import models
from apps.abstract.models import AbstractCommon


class Discipline(AbstractCommon):
    """Model for Discipline"""
    name = models.CharField("Nome da disciplina", max_length=150)
    workload = models.PositiveIntegerField("Carga horária")

    class Meta:
        verbose_name = 'Disciplina'

    def __str__(self):
        return self.name
