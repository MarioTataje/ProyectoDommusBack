from django.core.exceptions import ValidationError
from datetime import datetime
import pytz
# from django.utils.translation import gettext_lazy as _
# https://stackoverflow.com/questions/7366363/adding-custom-django-model-validation


def validate_is_string(value):
    if not (''.join(value.split())).isalpha():
        raise ValidationError('This field only suport alphabet letters.')


def validate_born_date(value):
    utc = pytz.UTC
    value = value.replace(tzinfo=utc)
    if value > datetime.today().replace(tzinfo=utc):
        raise ValidationError(
            'The born day can not be lower than the current date.')
