from rest_framework import serializers
from apps.abstract.schemas import AbstractModelSchema
from apps.discipline.models import Discipline


class AbstractDisciplineSchema(AbstractModelSchema, serializers.ModelSerializer):
    """Serializer and validate Discipline fields based on the model"""

    class Meta:
        model = Discipline
        fields = ['name', 'workload', 'create_user', 'update_user', 'created_at', 'updated_at', 'id']

    def validate(self, data):
        """Extend validator method to add custom validators"""

        name = data.get('name')
        workload = data.get('workload')
        if Discipline.objects.filter(name__exact=name, workload=workload).exists():
            raise serializers.ValidationError(['Já existem disciplina cadastrada com esse nome e carga horária'])
        return super(AbstractDisciplineSchema, self).validate(data)


class DisciplineSchema(AbstractDisciplineSchema):
    """Serializer and validate Discipline fields based on the model"""


class DisciplineUpdateSchema(AbstractDisciplineSchema):
    """Serializer and validate Discipline fields based on the model"""
