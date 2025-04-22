import os

from celery import (  # type: ignore
    Task,
    shared_task,
)
from core.models import SVGLifetimeSettings  # type: ignore
from django.conf import settings  # type: ignore
from django.test import RequestFactory  # type: ignore
from vtracer import convert_image_to_svg_py  # type: ignore


@shared_task(bind=True)
def convert_to_svg(self: Task, path_to_image: str, parameters: dict) -> None:

    path_to_svg = os.path.join(settings.MEDIA_ROOT, 'to_svg', f'{self.request.id}.svg')
    try:
        convert_image_to_svg_py(
            image_path=path_to_image,
            out_path=path_to_svg,

            colormode=parameters['color_mode'],

            filter_speckle=int(parameters['filter_speckle']),
            color_precision=int(parameters['color_precision']),
            layer_difference=int(parameters['layer_difference']),

            mode=parameters['mode'],

            corner_threshold=int(parameters['corner_threshold']),
            length_threshold=float(parameters['length_threshold']),
            splice_threshold=int(parameters['splice_threshold']),
            path_precision=int(parameters['path_precision']),

            max_iterations=10,
        )

    finally:

        request = RequestFactory().get('/')
        svg_lifetime_settings = SVGLifetimeSettings.load(request_or_site=request)
        remove_svg.apply_async(args=[path_to_image, path_to_svg], countdown=svg_lifetime_settings.lifetime * 60)


@shared_task
def remove_svg(path_to_image: str, path_to_svg: str) -> None:
    try:
        os.remove(path_to_image)
    except Exception:
        print('Source file already removed')

    try:
        os.remove(path_to_svg)
    except Exception:
        print('SVG file already removed')
