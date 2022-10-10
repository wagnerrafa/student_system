from django.http import JsonResponse
from rest_framework import permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.schemas.openapi import AutoSchema
from apps.abstract.views import AbstractViewApi
from apps.report_card.models import ReportCard
from apps.report_card.schemas import ReportCardSchema, ReportCardUpdateSchema


class ReportCardApi(AbstractViewApi):
    """HTTP methods for ReportCard"""

    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ['post', 'get']
    serializer_class = ReportCardSchema
    queryset = ReportCard.objects.all
    tag = ['report_card']
    schema = AutoSchema(tags=["Boletim"])

    query_params = [
        {
            "name": "nome_disciplina",
            "field": "discipline__name__icontains",
            "in": "query",
            "required": False,
            "placeholder": "teste",
            "description": "Nome da disciplina",
            "schema": {"type": "string"}
        },
        {
            "name": "nome_estudante",
            "field": "student__name__icontains",
            "in": "query",
            "required": False,
            "description": "Nome do estudante",
            "schema": {"type": "string"}
        },
        {
            "name": "nota",
            "field": "grade",
            "in": "query",
            "required": False,
            "description": "Nota do estudante",
            "schema": {"type": "int"}
        },
        {
            "name": "nota_gt",
            "field": "grade__gt",
            "in": "query",
            "required": False,
            "description": "Nota do estudante maior que",
            "schema": {"type": "int"}
        },
        {
            "name": "nota_lt",
            "field": "grade__lt",
            "in": "query",
            "required": False,
            "description": "Nota do estudante menor que",
            "schema": {"type": "int"}
        },
        {
            "name": "data_entrega",
            "field": "delivery_date",
            "in": "query",
            "required": False,
            "description": "Data de entrega do boletim",
            "schema": {"type": "date"}
        },
        {
            "name": "data_entrega_gt",
            "field": "delivery_date__gt",
            "in": "query",
            "required": False,
            "description": "Data de entrega do boletim maior que",
            "schema": {"type": "date"}
        },
        {
            "name": "data_entrega_lt",
            "field": "delivery_date__lt",
            "in": "query",
            "required": False,
            "description": "Data de entrega do boletim menor que",
            "schema": {"type": "date"}
        },
    ]

    def post(self, request, *args, **kwargs):
        """
           Create ReportCard receiving a dict
           return report_card detail
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_user = serializer.validated_data
        new_user['create_user'] = request.user.id
        report_card = ReportCard.objects.create(**new_user)
        return JsonResponse({'boletim': ReportCardSchema(report_card, many=False).data},
                            status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        """Get ReportCards details"""
        params = self.get_query_params()
        report_cards = self.queryset().filter(**params)
        report_cards = self.serializer_class(report_cards, many=True).data
        return JsonResponse({'boletins': report_cards})


class ReportCardEditApi(AbstractViewApi):
    """HTTP methods for ReportCard"""
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ['post', 'get', 'put', 'delete']
    serializer_class = ReportCardUpdateSchema
    queryset = ReportCard.objects.all
    schema = AutoSchema(tags=["Boletim"])

    def put(self, request, *args, **kwargs):
        """
           Update ReportCard information receiving a dict, return report_card detail
        """
        report_card_id = kwargs.get('id')
        report_card = get_object_or_404(ReportCard, id=report_card_id)
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        update_report_card = serializer.validated_data
        code = status.HTTP_200_OK
        if update_report_card:
            report_card.dict_update(**update_report_card)
            report_card.update_user = request.user.id
            report_card.save()
            code = status.HTTP_201_CREATED
        return JsonResponse({'boletim': ReportCardSchema(report_card, many=False).data}, status=code)

    def delete(self, request, *args, **kwargs):
        """Delete Boletim"""
        report_card_id = kwargs.get('id')
        report_card = get_object_or_404(ReportCard, id=report_card_id)
        report_card.delete()
        return JsonResponse({'detail': 'Boletim deletado'})
