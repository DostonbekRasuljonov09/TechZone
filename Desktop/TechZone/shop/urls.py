from django.urls import path
from .views import (index, product_detail,
                    cart_add, cart_remove, cart_update, cart_view,
                    checkout, order_success)

urlpatterns = [
    path('', index, name='index'),
    path('product/<slug:slug>/', product_detail, name='product_detail'),
    path('cart/', cart_view, name='cart'),
    path('cart/add/<int:product_id>/', cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', cart_remove, name='cart_remove'),
    path('cart/update/<int:product_id>/', cart_update, name='cart_update'),
    path('checkout/', checkout, name='checkout'),
    path('order/success/<int:order_id>/', order_success, name='order_success'),
]
