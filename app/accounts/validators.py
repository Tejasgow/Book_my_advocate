import re
from rest_framework import serializers


def password_validator(password):
    """
    Basic password rules:
    - Minimum 8 characters
    - At least 1 uppercase
    - At least 1 lowercase
    - At least 1 number
    """

    if len(password) < 8:
        raise serializers.ValidationError(
            "Password must be at least 8 characters long."
        )

    if not re.search(r"[A-Z]", password):
        raise serializers.ValidationError(
            "Password must contain at least one uppercase letter."
        )

    if not re.search(r"[a-z]", password):
        raise serializers.ValidationError(
            "Password must contain at least one lowercase letter."
        )

    if not re.search(r"\d", password):
        raise serializers.ValidationError(
            "Password must contain at least one number."
        )

    return password


def username_validator(username):
    """
    Basic username rule:
    - Must contain at least 1 uppercase letter
    """

    if not re.search(r"[A-Z]", username):
        raise serializers.ValidationError(
            "Username must contain at least one uppercase letter."
        )

    return username
