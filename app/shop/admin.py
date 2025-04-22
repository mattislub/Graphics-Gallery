from django.contrib import admin  # type: ignore

from shop.models import (
    BalanceProduct,
    ImageCategory,
    ImageOrientation,
    ImageProduct,
)

admin.site.register(ImageOrientation)
admin.site.register(BalanceProduct)
admin.site.register(ImageCategory)
admin.site.register(ImageProduct)
