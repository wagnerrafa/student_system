from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from rest_framework import serializers, renderers


class AbstractModelSchema(serializers.Serializer):
    """Serializer AbstractModel fields"""
    renderer_classes = [renderers.JSONRenderer]
    id = serializers.UUIDField(read_only=True)
    create_user = serializers.CharField(source='get_create_user', read_only=True)
    update_user = serializers.CharField(source='get_update_user', read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(allow_null=True, read_only=True)


class AbstractUpdateModelSchema(AbstractModelSchema):
    """Serializer AbstractModel fields"""

    def get_fields(self):
        fields = super(AbstractUpdateModelSchema, self).get_fields()
        request = self.context.get('request', None)
        if request and getattr(request, 'method', None) == "PUT":
            for key in fields.keys():
                setattr(fields[key], 'required', False)
        return fields


class UserSchema(serializers.ModelSerializer):
    """Serializer AbstractModel fields"""
    renderer_classes = [renderers.JSONRenderer]
    password = serializers.CharField(min_length=8, write_only=True, required=True)
    password_confirm = serializers.CharField(min_length=8, write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password', 'password_confirm']

    @staticmethod
    def __check_passwd(password, password_confirm):
        """Validate password is strong and same password confirm"""
        errors = []

        try:
            validate_password(password=password)
        except exceptions.ValidationError as e:
            errors = list(e.messages)

        if password != password_confirm:
            errors.append('As senhas não correspondem')
        return errors

    def validate(self, data):
        """Extend validator method to add custom validators"""

        password = data.get('password')
        password_confirm = data.get('password_confirm')
        errors = []
        errors.extend(self.__check_passwd(password, password_confirm))
        if errors:
            raise serializers.ValidationError(errors)
        return super(UserSchema, self).validate(data)
