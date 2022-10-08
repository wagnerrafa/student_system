from django.contrib.auth.models import User
from django.db import models
import uuid


class AbstractCommon(models.Model):
    """Abstraction of common fields in all models"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    create_user = models.UUIDField()
    update_user = models.UUIDField(null=True)

    class Meta:
        abstract = True

    @property
    def get_update_user(self):
        """Get update User by UUID"""
        if self.update_user:
            return self.__get_user(self.update_user)
        return ''

    @property
    def get_create_user(self):
        """Get create User by UUID"""
        if self.create_user:
            return self.__get_user(self.create_user)
        return ''

    @staticmethod
    def __get_user(id_):
        """Abstract get User by UUID"""
        user = User.objects.filter(id=id_).first()
        if user:
            return user.get_full_name()
        return ''

    def dict_update(self, *args, **kwargs):
        """Update model receiving a dict and changing attribute"""
        for name, values in kwargs.items():
            try:
                attr_value = getattr(self, name)
                if attr_value != values:
                    setattr(self, name, values)
            except KeyError:
                pass
        self.save()

    def __str__(self):
        return str(self.id)
