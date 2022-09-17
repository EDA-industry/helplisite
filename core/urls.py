from django.urls import path
from .views import HomeView, ProductView, ProductCreateView, ProductUpdateView, ProductDeleteView, add_product, cart, clear_cart

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('product/<pk>/<slug:slug>', ProductView.as_view(), name='product'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('cart/', cart, name="cart"),
    path('cart/<int:product_id>', add_product, name="cart_add_product"),
    path('cart/delete/', clear_cart, name="cart_clear"),
]