from django.apps import AppConfig

class AuthConfig(AppConfig):
    name = "apps.auth"
    label = "auth"
    verbose_name = "Auth"

    def ready(self):
        pass
