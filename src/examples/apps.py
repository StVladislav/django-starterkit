from django.apps import AppConfig


class TestConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.examples'
    
    def ready(self):
        """
        Enable django signals
        """
        import src.examples.receivers
