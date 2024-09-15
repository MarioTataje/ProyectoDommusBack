from django.apps import AppConfig


class SocialsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'socials'

    def ready(self):
        from .utils import prepare_model
        #prepare_model()
