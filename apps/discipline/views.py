from django.db.models import ProtectedError
from django.http import JsonResponse
from rest_framework import permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.schemas.openapi import AutoSchema
from apps.abstract.views import AbstractViewApi
from apps.discipline.models import Discipline
from apps.discipline.schemas import DisciplineSchema, DisciplineUpdateSchema


class DisciplineApi(AbstractViewApi):
    """HTTP methods for Discipline"""

    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ['post', 'get']
    serializer_class = DisciplineSchema
    queryset = Discipline.objects.all
    tag = ['discipline']
    schema = AutoSchema(tags=["Disciplina"])

    query_params = [
        {
            "name": "nome",
            "field": "name__icontains",
            "in": "query",
            "required": False,
            "description": "Nome da disciplina",
            "schema": {"type": "string"}
        },
        {
            "name": "carga_horaria",
            "field": "workload",
            "in": "query",
            "required": False,
            "description": "Carga horária da disciplina",
            "schema": {"type": "int"}
        },
    ]

    def post(self, request, *args, **kwargs):
        """
           Create Discipline receiving a dict
           return discipline detail
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_user = serializer.validated_data
        new_user['create_user'] = request.user.id
        discipline = Discipline.objects.create(**new_user)
        return JsonResponse({'disciplina': DisciplineSchema(discipline, many=False).data},
                            status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        """Get Disciplines details"""
        params = self.get_query_params()
        disciplines = self.queryset().filter(**params)
        disciplines = self.serializer_class(disciplines, many=True).data
        return JsonResponse({'disciplinas': disciplines})


class DisciplineEditApi(AbstractViewApi):
    """HTTP methods for Discipline"""
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ['post', 'get', 'put', 'delete']
    serializer_class = DisciplineUpdateSchema
    queryset = Discipline.objects.all
    schema = AutoSchema(tags=["Disciplina"])

    def put(self, request, *args, **kwargs):
        """
           Update Discipline information receiving a dict
           return discipline detail
        """
        discipline_id = kwargs.get('id')
        discipline = get_object_or_404(Discipline, id=discipline_id)
        serializer = self.serializer_class(data=request.data, context={'request': request, 'discipline': discipline})
        serializer.is_valid(raise_exception=True)
        update_user = serializer.validated_data
        code = status.HTTP_200_OK
        if update_user:
            discipline.dict_update(**update_user)
            discipline.update_user = request.user.id
            discipline.save()
            code = status.HTTP_201_CREATED
        return JsonResponse({'disciplina': DisciplineSchema(discipline, many=False).data}, status=code)

    def delete(self, request, *args, **kwargs):
        """Delete Disciplina if there is no reference to it"""
        discipline_id = kwargs.get('id')
        discipline = get_object_or_404(Discipline, id=discipline_id)
        try:
            discipline.delete()
            return JsonResponse({'detail': 'Disciplina deletada'})
        except ProtectedError:
            return JsonResponse(
                {'detail': 'Disciplina não deletada, há referências a ela e por isso não pode ser removida'})
