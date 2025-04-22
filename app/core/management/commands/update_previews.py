"""
Django command to wait for the Database to be available.
"""

from django.core.management.base import BaseCommand
from shop.models import ImageProduct


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Run updating previews..."))
        try:

            images = ImageProduct.objects.all()
            for i, image in enumerate(images):
                image.save()
                print(i)

        except Exception:
            self.stdout.write(self.style.NOTICE("An error occurred..."))
            return

        self.stdout.write(self.style.SUCCESS('All previews is updated.'))
