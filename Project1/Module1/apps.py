from django.apps import AppConfig

class Module1Config(AppConfig):
    name = 'Module1'

    def ready(self) -> None:
        import Module1.signals