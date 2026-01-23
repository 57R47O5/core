from rest_framework.authentication import BaseAuthentication

class OrcTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request._request.token  # seteado por middleware
        if not token:
            return None
        return (token.user, token)
