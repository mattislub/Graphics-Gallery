from django.urls import path  # type: ignore

from shop import views

urlpatterns = [
    path('user/purchase-subscription/', views.purchase_subscription),
    path('user/replenish-balance/', views.replenish_balance),

    path('api/quick-purchase/', views.quick_purchase),
    path('api/wishlist/count/', views.api_wishlist_count),
    path('api/wishlist/<str:code>/', views.api_wishlist),

    path('wishlist-preview/', views.wishlist_preview),
    path('basket-preview/', views.basket_preview),

    path('download/<str:token>/', views.download),
    path('download-by-subscription/<int:user_subscription_id>/<int:product_id>/', views.download_by_subscription),

    path('check-load-products/', views.check_load_products),
    path('newsletter/', views.newsletter),
]
