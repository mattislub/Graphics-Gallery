from __future__ import annotations

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from salesman.core.utils import get_salesman_model
from salesman.orders.models import BaseOrder, BaseOrderItem, BaseOrderPayment

from .filters import OrderIsPaidFilter, OrderStatusFilter
from .forms import OrderModelForm, OrderNoteModelForm
from .mixins import OrderAdminMixin, OrderAdminRefundMixin, OrderItemAdminMixin

Order = get_salesman_model("Order")
OrderItem = get_salesman_model("OrderItem")
OrderPayment = get_salesman_model("OrderPayment")
OrderNote = get_salesman_model("OrderNote")


class OrderItemInline(OrderItemAdminMixin, admin.TabularInline):
    model = OrderItem
    fields = [
        "name",
        "code",
        "total_display",
        "extra_display",
        "extra_rows_display",
    ]
    readonly_fields = fields

    def get_queryset(self, request: HttpRequest) -> QuerySet[BaseOrderItem]:
        self.model.request = request
        return super().get_queryset(request)

    def has_add_permission(
        self,
        request: HttpRequest,
        obj: BaseOrderItem | None = None,
    ) -> bool:
        return False

    def has_delete_permission(
        self,
        request: HttpRequest,
        obj: BaseOrderItem | None = None,
    ) -> bool:
        return False


class OrderPaymentInline(admin.TabularInline):
    model = OrderPayment
    fields = ["amount", "transaction_id", "payment_method", "date_created"]
    readonly_fields = ["amount", "transaction_id", "payment_method", "date_created"]
    extra = 0

    def has_add_permission(
        self,
        request: HttpRequest,
        obj: BaseOrderItem | None = None,
    ) -> bool:
        return False

    def get_queryset(self, request: HttpRequest) -> QuerySet[BaseOrderPayment]:
        self.model.request = request
        return super().get_queryset(request)


class OrderNoteInline(admin.TabularInline):
    model = OrderNote
    form = OrderNoteModelForm
    fields = ["message", "public", "date_created"]
    readonly_fields = ["date_created"]
    extra = 0


class OrderAdmin(OrderAdminMixin, OrderAdminRefundMixin, admin.ModelAdmin):
    """
    Default Order admin with refund functionality.
    """

    form = OrderModelForm
    change_form_template = "salesman/admin/change_form.html"
    date_hierarchy = "date_created"
    list_display = [
        "__str__",
        "email",
        "status_display",
        "total_display",
        "is_paid_display",
        "date_created",
    ]
    list_filter = [OrderStatusFilter, OrderIsPaidFilter, "date_created", "date_updated"]
    search_fields = ["ref", "email", "token"]
    readonly_fields = [
        "ref",
        "token",
        "status_display",
        "is_paid_display",
        "date_created",
        "date_updated",
        "customer_display",
        "email",
        "total_display",
        "amount_paid_display",
        "amount_outstanding_display",
        "extra_display",
        "extra_rows_display",
    ]
    fieldsets = [
        (_("Info"), {"fields": ["ref", "token"]}),
        (
            _("Status"),
            {"fields": ["status", "date_created", "date_updated", "is_paid_display"]},
        ),
        (
            _("Contact"),
            {
                "fields": [
                    "customer_display",
                    "email",
                ]
            },
        ),
        (
            _("Totals"),
            {
                "fields": [
                    "total_display",
                    "amount_paid_display",
                    "amount_outstanding_display",
                    "extra_rows_display",
                ]
            },
        ),
        (_("Extra"), {"fields": ["extra_display"]}),
    ]
    inlines = [OrderItemInline, OrderPaymentInline, OrderNoteInline]

    def get_queryset(self, request: HttpRequest) -> QuerySet[BaseOrder]:
        self.model.request = request
        return super().get_queryset(request)

    def has_add_permission(
        self,
        request: HttpRequest,
        obj: BaseOrder | None = None,
    ) -> bool:
        return False

    def has_delete_permission(
        self,
        request: HttpRequest,
        obj: BaseOrder | None = None,
    ) -> bool:
        return False


admin.site.register(Order, OrderAdmin)
