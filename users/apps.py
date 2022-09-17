from django.apps import AppConfig

class UsersConfig(AppConfig):
    name = 'users'

    # add this function
    def ready(self):
        from . import signals

# users/__init__.py 
default_app_config = 'users.apps.UsersConfig'