from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken


def blacklist_refresh_token(*, raw_token: str, user) -> None:
    try:
        token = RefreshToken(raw_token)
    except TokenError:
        raise ValidationError({
            "refresh_token": "Invalid or expired refresh token."
        })

    # Pastikan token dimiliki oleh pengguna yang sedang login.
    if str(token.get("user_id")) != str(user.pk):
        raise ValidationError({
            "refresh_token": "This token does not belong to this user."
        })

    try:
        token.blacklist()
    except TokenError:
        raise ValidationError({
            "refresh_token": "Unable to blacklist this token."
        })