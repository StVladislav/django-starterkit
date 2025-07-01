from django.apps import AppConfig


class TestConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src._test'
    
    def ready(self):
        """
        Enable django signals
        """
        import src._test.receivers
