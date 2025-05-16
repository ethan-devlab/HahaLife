# coding=utf-8

from django.urls import path
from .views.auth import auth
from .views.member import product, cart, checkout, purchase, notification
from .views.seller import seller, order, product as s_product
from .views.admin import admin, review, manage
from .views.applicant import applicant
from .views.shared import account

urlpatterns = [
    path('login/', auth.login_view, name='login'),
    path('applicant/login/', auth.applicant_view, name='applicant_login'),
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
    path('mypurchase/<str:oid>/review/<str:pid>/', purchase.submit_review, name='submit_member_review'),
    path('notification/', notification.notification_view, name='notification'),
    path('notification/read/<str:nid>/', notification.mark_read, name='mark_notification_read'),

    path('seller/add/', s_product.add_product, name='add_product'),
    path('seller/product/', s_product.manage_products, name='manage_products'),
    path('seller/product/<str:pid>/', s_product.product_detail_s, name='seller_product_detail'),
    path('seller/product/edit/<str:pid>/', s_product.edit_product, name='edit_product'),
    path('seller/product/delete/<str:pid>/', s_product.delete_product, name='delete_product'),
    path('seller/promotion/', s_product.add_promotion, name='add_promotion'),
    path('seller/order/', order.order_list, name='seller_order_list'),
    path('seller/order/<str:oid>/', order.order_detail_s, name='seller_order_detail'),
    path('seller/order/<str:oid>/review/<str:pid>/', order.submit_seller_review, name='submit_seller_review'),

    path('admin/review-applicant/', review.review_applicant, name='review_applicant'),
    path('admin/manage/user/', manage.manage_user, name='manage_user'),
    path('admin/manage/product/', manage.manage_product, name='manage_product'),

    path('new-seller/apply/', applicant.apply_view, name='apply'),
    path('new-seller/apply/success/', applicant.apply_success, name='apply_success'),
    path('new-seller/apply/status/', applicant.apply_status, name='apply_status'),
]
