from rest_framework import serializers
from apps.abstract.schemas import AbstractModelSchema, AbstractUpdateModelSchema
from apps.discipline.models import Discipline


class AbstractDisciplineSchema(serializers.ModelSerializer):
    """Serializer and validate Discipline fields based on the model"""

    class Meta:
        model = Discipline
        fields = ['name', 'workload', 'create_user', 'update_user', 'created_at', 'updated_at', 'id']


class DisciplineSchema(AbstractModelSchema, AbstractDisciplineSchema):
    """Serializer and validate Discipline fields based on the model"""

    def validate(self, data):
        """Extend validator method to add custom validators"""

        name = data.get('name')
        workload = data.get('workload')
        if Discipline.objects.filter(name__exact=name, workload=workload).exists():
            raise serializers.ValidationError(['Já existem disciplina cadastrada com esse nome e carga horária'])
        return super(AbstractDisciplineSchema, self).validate(data)


class DisciplineUpdateSchema(AbstractUpdateModelSchema, AbstractDisciplineSchema):
    """Serializer and validate Discipline fields based on the model"""

    def validate(self, data):
        """Extend validator method to add custom validators"""
        discipline = self.context.get('discipline')
        name = data.get('name') or discipline.name
        workload = data.get('workload') or discipline.workload
        if Discipline.objects.filter(name__exact=name, workload=workload).exists():
            raise serializers.ValidationError(['Já existem disciplina cadastrada com esse nome e carga horária'])
        return super(AbstractDisciplineSchema, self).validate(data)
