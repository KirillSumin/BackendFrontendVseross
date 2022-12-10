from django.core.validators import RegexValidator


validate_phone = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message='Номер телефона должен быть в формате \'+79999999999\''
)
