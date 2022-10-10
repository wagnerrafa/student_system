from django.db import models
from apps.abstract.models import AbstractCommon
from apps.discipline.models import Discipline
from apps.student.models import Student


class ReportCard(AbstractCommon):
    """Model for ReportCard"""
    discipline = models.ForeignKey(Discipline, on_delete=models.PROTECT)
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    grade = models.PositiveIntegerField("Nota do aluno")
    delivery_date = models.DateField('Data de entrega do boletim')

    class Meta:
        verbose_name = 'Boletim'

    def __str__(self):
        return f'Estudante: {self.student.name}, Disciplina: {self.discipline.name}, Nota: {self.grade}, ' \
               f'Entrega: {self.delivery_date}'
