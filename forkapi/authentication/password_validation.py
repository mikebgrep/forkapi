from django.contrib.auth.password_validation import get_default_password_validators
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status


def validate_password(password, user=None, password_validators=None):
    """
    Validate that the password meets all validator requirements.

    If the password is valid, return ``Response` 204 No Content` and save the new password .
    If the password is invalid, raise ValidationError with all error messages.
    """
    errors = []
    if password_validators is None:
        password_validators = get_default_password_validators()
    for validator in password_validators:
        try:
            validator.validate(password, user)
        except ValidationError as error:
            errors.append(error)
    if errors:
        return Response(data={"errors": [x for x in errors]}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(password)
    user.save()
    return Response(status=status.HTTP_204_NO_CONTENT)