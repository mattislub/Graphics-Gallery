from django.contrib import admin  # type: ignore
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin  # type: ignore
from django.contrib.auth.models import Group  # type: ignore
from django.db.models import QuerySet  # type: ignore
from django.http import HttpRequest  # type: ignore
from django.utils.safestring import mark_safe  # type: ignore
from django.utils.translation import gettext_lazy as _  # type: ignore

from core.models import (  # type: ignore
    Newsletter,
    User,
    Wishlist,
    WishlistImage,
)


class UserAdmin(DefaultUserAdmin):
    model = User
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'is_active', 'verification_code', 'registration_date')}),
        (_('Notifications'), {'fields': ('balance_replenishment_notification', 'purchase_notification', 'filled_cart_notification')}),
        (None, {'fields': ('balance', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'password1', 'password2'),
        }),
    )

    ordering = ('email', )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff')
    readonly_fields = ('balance', 'verification_code', 'registration_date')


class WishlistItemInline(admin.TabularInline):
    model = WishlistImage
    fields = ('get_image_html', )
    readonly_fields = ('get_image_html', )

    def get_image_html(self, obj: WishlistImage) -> str:
        return mark_safe(str(obj.image))  # noqa S308

    get_image_html.short_description = 'Image'  # type: ignore

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        self.model.request = request
        return super().get_queryset(request)

    def has_add_permission(self, request: HttpRequest, obj: WishlistImage | None = None) -> bool:
        return False

    def has_delete_permission(self, request: HttpRequest, obj: WishlistImage | None = None) -> bool:
        return False


class WishlistAdmin(admin.ModelAdmin):
    model = Wishlist
    fields = ('user', )
    readonly_fields = ('user', )
    inlines = (WishlistItemInline, )

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        self.model.request = request
        return super().get_queryset(request)

    def has_add_permission(self, request: HttpRequest, obj: Wishlist | None = None) -> bool:
        return False

    def has_delete_permission(self, request: HttpRequest, obj: Wishlist | None = None) -> bool:
        return False


admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Newsletter)
