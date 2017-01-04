import datetime
from django.utils.timezone import utc
from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions
from rest_framework.authtoken.models import Token


class ExpiringTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token.')

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted.')

        utc_now = datetime.datetime.utcnow().replace(tzinfo=utc)

        if token.created < utc_now - datetime.timedelta(hours=24):
            print("Token has expired")
            raise exceptions.AuthenticationFailed('Token has expired')
        print("user " + token.user.username)
        return token.user, token
