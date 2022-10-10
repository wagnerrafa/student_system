import datetime
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import generics, status, serializers
from rest_framework.filters import BaseFilterBackend
from rest_framework.schemas.openapi import AutoSchema
from apps.abstract.schemas import UserSchema
from apps.permissions.views import IsAuthenticatedOrWriteOnly


def view_404(request, exception=None):
    return redirect('api-docs')


class UserApi(generics.GenericAPIView):
    """HTTP methods for Student"""
    permission_classes = (IsAuthenticatedOrWriteOnly,)
    http_method_names = ['post', 'get', 'put', 'delete']
    serializer_class = UserSchema
    schema = AutoSchema(tags=["User"])

    def post(self, request, *args, **kwargs):
        """
           Create User receiving a dict, return user detail
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_user = serializer.validated_data
        new_user.pop('password_confirm', None)
        password = new_user.pop('password', None)
        user = User.objects.create_user(**new_user)
        user.set_password(password)
        user.save()
        self.__authenticate_user(new_user['username'], password)
        return JsonResponse({'user': UserSchema(user, many=False).data}, status=status.HTTP_201_CREATED)

    def __authenticate_user(self, username, password):
        """Authenticate user for API documentation and tests"""
        user_authenticated = authenticate(username=username, password=password)
        if user_authenticated:
            login(self.request, user_authenticated)

    def __alter_password(self, old_password, new_password):
        """Change password on update"""
        check_old_password = self.request.user.check_password(old_password)
        if check_old_password:
            self.request.user.set_password(new_password)
            self.request.user.save()
            self.__authenticate_user(self.request.user.username, new_password)
            return
        raise serializers.ValidationError(['Senha antiga invalida'])


class SimpleFilterBackend(BaseFilterBackend):
    def get_schema_operation_parameters(self, view):
        return view.query_params


class AbstractViewApi(generics.GenericAPIView):
    """HTTP methods for Student"""
    filter_backends = (SimpleFilterBackend,)
    query_params = []

    @staticmethod
    def get_schema_operation_parameters(view):
        return view.query_params

    @staticmethod
    def __parse_date(date_string):
        """Parse sting to date"""
        return datetime.datetime.strptime(date_string, '%Y-%m-%d').date()

    @staticmethod
    def __parse_datetime(date_string):
        """Parse sting to datetime"""
        return datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M')

    def __get_type_by_instance(self, instance):
        """Get instance, type, parser and legend by field schema type"""
        types = {
            'string': {'type': str, 'parser': str, 'legend': 'string'},
            'date': {'type': datetime.date, 'parser': self.__parse_date, 'legend': '2001-12-30'},
            'datetime': {'type': datetime.date, 'parser': self.__parse_datetime, 'legend': '2001-12-30 23:01'},
            'float': {'type': float, 'parser': float, 'legend': '01.00'},
            'int': {'type': int, 'parser': int, 'legend': '1'},
        }

        return types.get(instance, str)

    def get_query_params(self):
        """Validate parameters received in query params, returning query values"""
        query = {}
        for valid_params in self.query_params:
            type_instance = valid_params['schema']['type']
            field = valid_params['field']
            name = valid_params['name']
            value = self.request.query_params.get(name)
            if value:
                instance = self.__get_type_by_instance(type_instance)
                try:
                    value = instance['parser'](value)
                except:
                    pass
                if isinstance(value, instance['type']):
                    query[field] = value
                else:
                    raise serializers.ValidationError(
                        {name: f'Campo no formato inválido. Deve ser estar no formato {instance["legend"]}'})
        return query
