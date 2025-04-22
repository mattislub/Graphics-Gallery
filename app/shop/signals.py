import os
from typing import Type

from django.conf import settings  # type: ignore
from django.db.models.signals import (  # type: ignore
    post_save,
    pre_delete,
)
from django.dispatch import receiver  # type: ignore
from PIL import Image  # type: ignore

from shop.models import ImageProduct
from shop.utils import watermark


@receiver(post_save, sender=ImageProduct)
def create_thumbnail(sender: Type[ImageProduct], instance: ImageProduct, created: bool, **kwargs) -> None:
    mask = Image.open(os.path.join(settings.STATIC_ROOT, 'media', 'mask.png')).resize((800, 800), resample=Image.LANCZOS)

    display_image = Image.open(os.path.join(settings.MEDIA_ROOT, instance.image.name)).convert('RGBA')
    display_image.thumbnail((800, 800), resample=Image.LANCZOS)
    display_image = watermark(
        display_image,
        mask,
        scale=.6,
        opacity=.5,
        position='C',
    )
    display_image.save(os.path.join(settings.MEDIA_ROOT, 'previews', instance.display_image_name))

    preview_image = Image.open(os.path.join(settings.MEDIA_ROOT, instance.image.name)).convert('RGBA')
    preview_image.thumbnail((400, 400), resample=Image.LANCZOS)
    preview_image = watermark(
        preview_image,
        mask,
        scale=.3,
        opacity=.5,
        position='C',
    )
    preview_image.save(os.path.join(settings.MEDIA_ROOT, 'previews', instance.preview_image_name))


@receiver(pre_delete, sender=ImageProduct)
def delete_images(sender: Type[ImageProduct], instance: ImageProduct, **kwargs) -> None:
    try:
        os.remove(os.path.join(settings.MEDIA_ROOT, 'previews', instance.display_image_name))
    except FileNotFoundError:
        pass
    try:
        os.remove(os.path.join(settings.MEDIA_ROOT, 'previews', instance.preview_image_name))
    except FileNotFoundError:
        pass
    try:
        os.remove(os.path.join(settings.MEDIA_ROOT, instance.image.name))
    except FileNotFoundError:
        pass
