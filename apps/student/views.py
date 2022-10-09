from django.http import JsonResponse
from rest_framework import permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.schemas.openapi import AutoSchema
from apps.abstract.views import AbstractViewApi
from apps.student.models import Student
from apps.student.schemas import StudentSchema, StudentUpdateSchema


class StudentApi(AbstractViewApi):
    """HTTP methods for Student"""
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ['post', 'get']
    serializer_class = StudentSchema
    queryset = Student.objects.all
    schema = AutoSchema(tags=["Estudante"])
    query_params = [
        {
            "name": "nome",
            "field": "name",
            "in": "query",
            "required": False,
            "description": "Nome do aluno",
            "schema": {"type": "string"}
        },
        {
            "name": "data_nascimento",
            "field": "birthday",
            "in": "query",
            "required": False,
            "description": "Data de nascimento do aluno",
            "schema": {"type": "date"}
        },
        {
            "name": "email",
            "field": "email",
            "in": "query",
            "required": False,
            "description": "Email do aluno",
            "schema": {"type": "string"}
        },
    ]

    def post(self, request, *args, **kwargs):
        """
           Create Student receiving a dict
           return student detail
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_user = serializer.validated_data
        new_user['create_user'] = request.user.id
        student = Student.objects.create(**new_user)
        return JsonResponse({'aluno': StudentSchema(student, many=False).data}, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        """Get Students details"""
        params = self.get_query_params()
        students = self.queryset().filter(**params)
        students = self.serializer_class(students, many=True).data
        return JsonResponse({'alunos': students})


class StudentEditApi(AbstractViewApi):
    """HTTP methods for Student"""
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ['post', 'get', 'put', 'delete']
    serializer_class = StudentUpdateSchema
    queryset = Student.objects.all
    schema = AutoSchema(tags=["Estudante"])

    def put(self, request, *args, **kwargs):
        """
           Update Student information receiving a dict
           return student detail
        """
        student_id = kwargs.get('id')
        student = get_object_or_404(Student, id=student_id)
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        update_user = serializer.validated_data
        code = status.HTTP_200_OK
        if update_user:
            student.dict_update(**update_user)
            student.update_user = request.user.id
            student.save()
            code = status.HTTP_201_CREATED
        return JsonResponse({'aluno': StudentSchema(student, many=False).data}, status=code)

    def delete(self, request, *args, **kwargs):
        """Delete User"""
        # TODO: remove other models when they are built
        student_id = kwargs.get('id')
        student = get_object_or_404(Student, id=student_id)
        if student:
            student.delete()
        return JsonResponse({'detail': 'Aluno deletado'})
