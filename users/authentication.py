import datetime

import pytz
from django.conf import settings
from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed


class ExpiringTokenAuthentication(TokenAuthentication):
    model = Token

    def authenticate_credentials(self, key, request=None):
        models = self.get_model()

        try:
            token = models.objects.select_related("user").get(key=key)
        except models.DoesNotExist:
            raise AuthenticationFailed(
                {"error": "Invalid or Inactive Token", "is_authenticated": False}
            )

        if not token.user.is_active:
            raise AuthenticationFailed(
                {"error": "Invalid user", "is_authenticated": False}
            )

        utc_now = timezone.now()
        utc_now = utc_now.replace(tzinfo=pytz.utc)

        if token.created < utc_now - datetime.timedelta(minutes=settings.TOKEN_EXPIRATION_MINUTES):
            raise AuthenticationFailed(
                {"expired_token_error": ["Token has expired"]}
            )
        return token.user, token
