from django.apps import AppConfig


class CosellappConfig(AppConfig):
    name = 'CosellApp'
    def ready(self):
        import CosellApp.signals
    
