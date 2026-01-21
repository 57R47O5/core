import threading

_local = threading.local()

def get_current_username():
    return getattr(_local, "username", "system")


class CurrentUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user and request.user.is_authenticated:
            _local.username = request.user.username
        else:
            _local.username = "anonymous"

        response = self.get_response(request)
        return response
