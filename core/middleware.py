from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.exceptions import AuthenticationFailed
from django.utils.encoding import smart_str
from rest_framework_simplejwt.tokens import AccessToken

class JWTCookieAuthentication(JWTAuthentication):
    """
    Custom JWT authentication that supports token in cookies
    """
    def authenticate(self, request):
        # First, try to get the token from the Authorization header
        header = self.get_header(request)
        
        if header is not None:
            # If Authorization header is present, use it
            return super().authenticate(request)
            
        # If no Authorization header, try to get token from cookie
        raw_token = request.COOKIES.get('access_token')
        if raw_token is None:
            return None
            
        # Validate the token directly without recursion
        try:
            validated_token = self.get_validated_token(raw_token)
            return self.get_user(validated_token), validated_token
        except (InvalidToken, TokenError) as e:
            raise AuthenticationFailed(str(e))
    
    def get_validated_token(self, raw_token):
        """
        Validates token and returns a validated token wrapper object.
        """
        try:
            # Create a token object from the raw token
            token = AccessToken(token=raw_token)
            # Verify the token's signature and expiration
            token.verify()
            return token
        except Exception as e:
            raise InvalidToken(str(e))
