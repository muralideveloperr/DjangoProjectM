from django.apps import AppConfig
from django.db.models.signals import post_migrate


class ProjectmConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'projectM'

    def ready(self):
        from projectM.signals import create_groups_permission
        post_migrate.connect(create_groups_permission)
