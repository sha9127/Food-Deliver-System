from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import CustomUserManager
import uuid

# Create your models here.


class BaseModel(models.Model):

    class Meta:
        abstract = True
    objects = models.Manager()
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    deleted_date = models.DateTimeField(blank=True, null=True)


class Role(BaseModel):

    name = models.CharField(max_length=10, default=None,
                            blank=False, null=False)

    def __str__(self):
        return self.name


class User(AbstractBaseUser, BaseModel):

    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    role = models.ForeignKey(
        Role, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(default='default.jpg', upload_to='user')

    # is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    # REQUIRED_FIELD = []

    def __str__(self):
        """
        String representation of name
        :return:
        """
        return "{}-{}".format(self.email, self.id)

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # All admins are staff
        return self.is_admin

    @staticmethod
    def update_instance(data):
        return User.objects.update(**data)
