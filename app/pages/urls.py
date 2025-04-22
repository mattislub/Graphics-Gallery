from django.urls import path  # type: ignore

from pages import views

urlpatterns = [
    path('user/resend-contact-us-form/', views.resend_contact_us_form),

    path('user/profile/', views.user_profile, name='user-profile'),
    path('user/transactions/', views.user_transactions, name='user-transactions'),
    path('user/wishlist/', views.user_wishlist, name='user-wishlist'),
    path('user/purchases/', views.user_purchases, name='user-purchases'),

    path('user/registration/', views.user_registration, name='registration'),
    path('user/login/', views.user_login, name='login'),
    path('user/email-verification/', views.email_verification, name='verify-email'),
    path('user/logout/', views.user_logout),

    path('to-svg/', views.to_svg, name='to-svg'),
    path('download-svg/<str:key>/', views.download_svg, name='download-svg'),
    path('get-svg-conversion-status/<str:key>/', views.get_svg_conversion_status, name='get-svg-conversion-status'),
]
