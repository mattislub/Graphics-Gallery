from django.apps import AppConfig  # type: ignore


class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop'

    def ready(self) -> None:
        import shop.signals  # noqa F401

        return super().ready()
