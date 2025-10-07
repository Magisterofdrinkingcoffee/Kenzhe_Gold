from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic import RedirectView
from store import views

urlpatterns = [
    path("admin/", admin.site.urls),

    # --- Главная и каталог ---
    path("", views.home, name="home"),
    path("products/", views.products_list, name="products_list"),
    path("products/<int:pk>/", views.product_detail, name="product_detail"),
    path("type/<int:type_id>/", views.products_by_type, name="products_by_type"),

    # --- Корзина и заказы ---
    path("cart/", views.cart_view, name="cart"),
    path("cart/add/<int:pk>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:pk>/", views.remove_from_cart, name="remove_from_cart"),
    path("cart/increase/<int:pk>/", views.increase, name="increase"),
    path("checkout/", views.checkout, name="checkout"),
    path("order/success/", views.order_success, name="order_success"),

    # --- Редиректы на allauth (твои старые страницы остаются) ---
    path("login/", RedirectView.as_view(pattern_name="account_login"), name="login"),
    path("register/", RedirectView.as_view(pattern_name="account_signup"), name="register"),
    path("logout/", RedirectView.as_view(pattern_name="account_logout"), name="logout"),
    path("accounts/", include("allauth.urls")),

    # --- Allauth (всё управление учётками) ---
    path("accounts/", include("allauth.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
