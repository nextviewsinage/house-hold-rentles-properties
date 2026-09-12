from django.contrib import admin
from django.urls import path,include
from ownerapp import views


urlpatterns = [
    path('index/',views.indexview,name='index'),
    path('portfolio-detail/',views.portfoliodetailsview,name='portfolio-detail'),
    path('inner-page/',views.innerpageview,name='inner-page'),
    path('forms/',views.formsview,name='forms'),
    path('login2/',views.login2view,name='login2'),
    path('logout2/',views.logout2view,name='logout2'),
    path('register/',views.regsiteriew,name='register'),
    path('tableview/',views.tableview,name='tableview'),
    path('deleteproduct/<int:id>/',views.deleteproduct,name='deleteproduct'),
    path('editproduct/<int:id>/',views.editproduct,name='editproduct'),
    path('updateproduct/<int:id>/',views.updateproduct,name='updateproduct'),
    path('product/',views.productview,name='product'),
    # path('confirm_order/',views.confirm_order_view,name='confirm_order_view'),
    path('category/',views.category,name='category'),
    path('tablecategory/',views.tablecategoryview,name='tablecategory'),
    path('deletecategory/<int:id>/',views.deletecategory,name='deletecategory'),
    path('editcategory/<int:id>/',views.editcategory,name='editcategory'),
    path('updatecategory/<int:id>/',views.updatecategory,name='updatecategory'),
    path('changepassword/',views.changepass1wordview,name='changepassword'),
    # path('cart/add/<int:id>/',views.cart_add,name='cart_add'),
    # path('cart/item_clear/<int:id>/',views.item_clear, name='item_clear'),
    # path('cart/item_increment/<int:id>/',views.item_increment,name='item_increment'),
    # path('cart/item_decrement/<int:id>/',views.item_decrement,name='item_decrement'),
    # path('cart/cart_clear/',views.cart_clear,name='cart_clear'),
    # path('cart/cart-detail/',views.cart_detail,name='cart_detail'),
    # path('add_to_cart/',views.add_to_cart,name='add_to_cart'),
    # path('serachcategory/<str:name>/',views.serachcategory,name='serachcategory'),

]
