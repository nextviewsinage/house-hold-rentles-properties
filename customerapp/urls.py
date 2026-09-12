from django.contrib import admin
from django.urls import path, include
from customerapp import views

urlpatterns = [
    # --- Existing URLs (unchanged) ---
    path('index2view/', views.index2view, name='index2view'),
    path('portfolio-detail/', views.portfoliodetailsview, name='portfolio-detail'),
    path('inner-page/', views.innerpageview, name='inner-page'),
    path('blog-html/', views.blogview, name='blog-html'),
    path('blog-single/', views.blogsingleview, name='blog-single'),
    path('login1/', views.login1view, name='login1'),
    path('logout1/', views.logout1view, name='lout'),
    path('register1/', views.regsiter1view, name='re'),
    path('feedback/', views.feedbackview, name='feedback'),
    path('table/', views.tableview, name='table'),
    path('deletefeedback/<int:id>/', views.deletefeedback, name='deletefeedback'),
    path('editfeedback/<int:id>/', views.editfeedback, name='editfeedback'),
    path('updatefeedback/<int:id>/', views.updatefeedback, name='updatefeedback'),
    path('confirm_order/', views.confirm_order_view, name='confirm_order_view'),
    path('order_success/', views.order_successview, name='order_success'),
    path('My_order/', views.my_orders_view, name='My_order'),
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/', views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/', views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/', views.cart_detail, name='cart_detail'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('serachcategory/<str:name>/', views.serachcategory, name='serachcategory'),
    path('generate_invoice/<int:order_id>/', views.generate_invoice, name='generate_invoice'),
    path('changepassword/', views.changepasswordview, name='changepassword'),

    # --- New URLs ---
    path('product/<int:id>/', views.product_detail_view, name='product_detail'),
    path('search/', views.product_search_view, name='product_search'),
    path('sort/', views.price_sort_view, name='price_sort'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/toggle/<int:id>/', views.wishlist_toggle, name='wishlist_toggle'),
    path('order/cancel/<int:order_id>/', views.cancel_order_view, name='cancel_order'),
    path('order/tracking/<int:order_id>/', views.order_tracking_view, name='order_tracking'),
    path('profile/', views.customer_profile_view, name='customer_profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
]
