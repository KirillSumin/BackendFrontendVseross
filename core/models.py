from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.core.validators import validate_email

from core.validators import validate_phone


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_operator(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email', validators=[validate_email], unique=True, db_index=True)
    is_email_valid = models.BooleanField('email проверен', default=False)
    email_valid_d = models.DateTimeField('дата последней валидации email', null=True, blank=True)

    phone = models.CharField('номер телефона', validators=[validate_phone], max_length=17, blank=True, null=True)
    is_phone_valid = models.BooleanField('номер телефона проверен', default=False)
    phone_valid_d = models.DateTimeField('дата последней валидации телефона', null=True, blank=True)

    first_name = models.CharField('имя', max_length=150)
    last_name = models.CharField('фамилия', max_length=150)
    patronymic = models.CharField('отчество', max_length=150, blank=True)

    is_staff = models.BooleanField('персонал?', default=False)

    created_d = models.DateTimeField('дата создания', default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"

    def get_full_name(self):
        return f'{self.last_name} {self.first_name} #{self.id}'

    def __str__(self):
        # бесполезная тема если first_name last_name обязательны
        if self.first_name or self.last_name:
            return self.get_full_name()
        return f'{self.email} #{self.id}'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
