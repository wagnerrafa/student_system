from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import generics, status, serializers
from rest_framework.filters import BaseFilterBackend

from apps.abstract.schemas import UserSchema
from apps.permissions.views import IsAuthenticatedOrWriteOnly


def view_404(request, exception=None):
    return redirect('api-docs')


class UserApi(generics.GenericAPIView):
    """HTTP methods for Student"""
    permission_classes = (IsAuthenticatedOrWriteOnly,)
    http_method_names = ['post', 'get', 'put', 'delete']
    serializer_class = UserSchema

    def post(self, request, *args, **kwargs):
        """
           Create User receiving a dict
           return user detail
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

    def get_query_params(self):
        """Validate parameters received in query params, returning query values"""
        query = {}

        for valid_params in self.query_params:
            value = self.request.query_params.get(valid_params['name'])
            if value:
                query[valid_params['field']] = value
        return query
