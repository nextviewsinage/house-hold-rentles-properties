from django.contrib import admin
from django.urls import path,include
from customerapp import views



urlpatterns = [
    path('index2view/',views.index2view,name='index2view'),
    path('portfolio-detail/',views.portfoliodetailsview,name='portfolio-detail'),
    path('inner-page/',views.innerpageview,name='inner-page'),
    path('blog-html/',views.blogview,name='blog-html'),
    path('blog-single/',views.blogsingleview,name='blog-single'),
    path('login1/',views.login1view,name='login1'),
    path('logout1/',views.logout1view,name='lout'),
    path('register1/',views.regsiter1view,name='re'),
    path('feedback/',views.feedbackview,name='feedback'),
    path('table/',views.tableview,name='table'),
    path('deletefeedback/<int:id>/',views.deletefeedback,name='deletefeedback'),
    path('editfeedback/<int:id>/',views.editfeedback,name='editfeedback'),
    path('updatefeedback/<int:id>/',views.updatefeedback,name='updatefeedback'),
    path('confirm_order/',views.confirm_order_view,name='confirm_order_view'),
    path('order_success/',views.order_successview,name='order_success'),
    path('My_order/',views.my_orders_view,name='My_order'),
    # path('category/',views.category,name='category'),
    # path('tablecategory/',views.tablecategoryview,name='tablecategory'),
    # path('deletecategory/<int:id>/',views.deletecategory,name='deletecategory'),
    # path('editcategory/<int:id>/',views.editcategory,name='editcategory'),
    # path('updatecategory/<int:id>/',views.updatecategory,name='updatecategory'),
    path('cart/add/<int:id>/',views.cart_add,name='cart_add'),
    path('cart/item_clear/<int:id>/',views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',views.item_increment,name='item_increment'),
    path('cart/item_decrement/<int:id>/',views.item_decrement,name='item_decrement'),
    path('cart/cart_clear/',views.cart_clear,name='cart_clear'),
    path('cart/cart-detail/',views.cart_detail,name='cart_detail'),
    path('add_to_cart/',views.add_to_cart,name='add_to_cart'),
    path('serachcategory/<str:name>/',views.serachcategory,name='serachcategory'),
    path('generate_invoice/<int:order_id>/', views.generate_invoice, name='generate_invoice'),
    path('changepassword/',views.changepasswordview,name='changepassword'),
]

   





