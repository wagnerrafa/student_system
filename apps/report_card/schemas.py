from rest_framework import serializers
from apps.abstract.schemas import AbstractModelSchema, AbstractUpdateModelSchema
from apps.discipline.models import Discipline
from apps.discipline.schemas import DisciplineSchema
from apps.report_card.models import ReportCard
from apps.student.models import Student
from apps.student.schemas import StudentSchema


class AbstractReportCardSchema(serializers.ModelSerializer):
    """Serializer and validate ReportCard fields based on the model"""

    discipline = DisciplineSchema(many=False, read_only=True)
    student = StudentSchema(many=False, read_only=True)
    discipline_id = serializers.UUIDField(write_only=True)
    student_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = ReportCard
        fields = ['discipline', 'student', 'grade', 'delivery_date', 'create_user', 'update_user', 'created_at',
                  'updated_at', 'id', 'discipline_id', 'student_id']


class ReportCardSchema(AbstractModelSchema, AbstractReportCardSchema):
    """Serializer and validate ReportCard fields based on the model"""

    def validate(self, data):
        """Extend validator method to add custom validators"""
        erros = []
        discipline_id = data.get('discipline_id')
        student_id = data.get('student_id')
        if Discipline.objects.filter(id=discipline_id).exists() is False:
            erros.append({'discipline_id': 'Não foi encontrado a disciplina com esse id'})
        if Student.objects.filter(id=student_id).exists() is False:
            erros.append({'student_id': 'Não foi encontrado o aluno com esse id'})
        if erros:
            raise serializers.ValidationError(erros)
        return super(AbstractReportCardSchema, self).validate(data)


class ReportCardUpdateSchema(AbstractUpdateModelSchema, AbstractReportCardSchema):
    """Serializer and validate ReportCard fields based on the model"""

    def validate(self, data):
        """Extend validator method to add custom validators"""
        erros = []
        discipline_id = data.get('discipline_id')
        student_id = data.get('student_id')
        if discipline_id and Discipline.objects.filter(id=discipline_id).exists() is False:
            erros.append({'discipline_id': 'Não foi encontrado a disciplina com esse id'})
        if student_id and Student.objects.filter(id=student_id).exists() is False:
            erros.append({'student_id': 'Não foi encontrado o aluno com esse id'})
        if erros:
            raise serializers.ValidationError(erros)
        return super(AbstractReportCardSchema, self).validate(data)
