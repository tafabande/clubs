from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import exceptions

class CookieJWTAuthentication(JWTAuthentication):
    """
    Custom authentication class that reads JWT from httpOnly cookies.
    """
    def authenticate(self, request):
        header = self.get_header(request)
        
        if header is None:
            # If no header, try to get from cookie
            raw_token = request.COOKIES.get('access_token')
        else:
            raw_token = self.get_raw_token(header)

        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        return self.get_user(validated_token), validated_token
