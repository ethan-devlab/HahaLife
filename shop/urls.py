# coding=utf-8

from django.urls import path
from .views import auth, member, seller, admin, product, cart, checkout, purchase, account, notification

urlpatterns = [
    path('login/', auth.login_view, name='login'),
    path('register/', auth.register_view, name='register'),
    path('logout/', auth.logout_view, name='logout'),
    path('guest/', auth.guest_view, name='guest'),

    # path('member/', member.dashboard, name='member_dashboard'),
    path('seller/', seller.dashboard, name='seller_dashboard'),
    path('admin/', admin.dashboard, name='admin_dashboard'),

    path('myaccount/', account.account_view, name='account'),
    path('myaccount/update/', account.update_account, name='update_account'),

    path('', product.product_list, name='product_list'),
    path('products/<str:pid>/', product.product_detail, name='product_detail'),
    path('cart/', cart.view_cart, name='view_cart'),
    path('cart/add/', cart.add_to_cart, name='add_to_cart'),
    path('cart/delete/<str:pid>/', cart.delete_from_cart, name='delete_from_cart'),
    path('cart/update/<str:pid>/', cart.update_quantity, name='update_quantity'),
    path('checkout/', checkout.checkout_view, name='checkout'),
    path('checkout/place/', checkout.place_order, name='place_order'),
    path('mypurchase/', purchase.purchase_list, name='mypurchase'),
    path('mypurchase/<str:oid>/', purchase.purchase_detail, name='purchase_detail'),
    path('mypurchase/<str:oid>/cancel/', purchase.cancel_order, name='cancel_order'),
    path('mypurchase/<str:oid>/review/<str:pid>/', purchase.submit_review, name='submit_review'),
    path('notification/', notification.notification_view, name='notification'),
    path('notification/read/<str:nid>/', notification.mark_read, name='mark_notification_read'),
]
