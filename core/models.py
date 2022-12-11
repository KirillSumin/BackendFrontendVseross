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

    car_number = models.CharField('номер авто', max_length=10, null=True, blank=True)

    user_photo = models.ImageField('фото пользователя', upload_to='users_photos')

    is_staff = models.BooleanField('персонал?', default=False)

    created_d = models.DateTimeField('дата создания', default=timezone.now)

    def is_verified(self):
        return True

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


class EntranceHistory(models.Model):
    AUTH_TYPE = [
        ('auto', 'AutoNumber'),
        ('face', 'FaceRecognition'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='id связанного юзера', related_name='entrance_story')

    auth_type = models.CharField(
        max_length=4,
        choices=AUTH_TYPE,
    )

    entry_date = models.DateTimeField('дата входа', auto_now_add=True)
    exit_date = models.DateTimeField('дата выхода', blank=True, null=True)

    def __str__(self):
        if not self.exit_date:
            exit_date_str = 'Ещё не вышел'
        else:
            exit_date_str = self.exit_date.strftime("%d-%m-%Y")
        return f'#{self.user_id} {self.entry_date.strftime("%d-%m-%Y")} {exit_date_str}'

    class Meta:
        verbose_name = 'История входа и выхода'
        verbose_name_plural = 'Истории входа и выхода'
