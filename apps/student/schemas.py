from rest_framework import serializers
from apps.abstract.schemas import AbstractModelSchema, AbstractUpdateModelSchema
from apps.student.models import Student

fields = ['email', 'name', 'birthday', 'create_user', 'update_user', 'created_at', 'updated_at', 'id']


class StudentSchema(AbstractModelSchema, serializers.ModelSerializer):
    """Serializer and validate Student fields based on the model"""

    class Meta:
        model = Student
        fields = fields


class StudentUpdateSchema(AbstractUpdateModelSchema, serializers.ModelSerializer):
    """Serializer and validate Student fields based on the model"""

    class Meta:
        model = Student
        fields = fields
