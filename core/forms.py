from django import forms
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    email = forms.EmailField(
        label='Email', max_length=255
    )
    password = forms.RegexField(
        # TODO нормальный regex на проде
        label='Пароль', regex=r'^[a-zA-Z0-9]{1,255}$', strip=True,
        error_messages={'invalid': (
            'Тут должно быть про 8 символов и тд '
        )}, max_length=255
    )
