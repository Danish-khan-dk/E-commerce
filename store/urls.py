from django.urls import path
from .import views as v 

urlpatterns = [
    path("",v.index),
    path("shop",v.shop,name="shop"),
    path("about",v.about),
    path("contact",v.contact),
    path("register",v.register),
    path("login",v.login),
    path("product/<str:id>",v.product_details),
    path("logout",v.logout),
    path("search",v.search),
    path("success",v.success,name="success"),
    path("your_order",v.your_order,name="your_order"),
    # ======== cart =========
    path('cart/add/<int:id>/', v.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', v.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',
         v.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',
         v.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', v.cart_clear, name='cart_clear'),
    path('cart/cart-detail/',v.cart_detail,name='cart_detail'),
    path('checkout',v.checkout,name='checkout'),
    path('placeorder',v.placeorder,name='placeorder'),

]