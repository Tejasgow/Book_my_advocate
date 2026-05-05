from rest_framework_simplejwt.authentication import JWTAuthentication


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # First, try to get token from cookie
        raw_token = request.COOKIES.get("access_token")
        
        # If no cookie token, try to get from Authorization header
        if raw_token is None:
            auth_header = request.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                raw_token = auth_header[7:]  # Remove "Bearer " prefix
        
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        user = self.get_user(validated_token)

        return user, validated_token
