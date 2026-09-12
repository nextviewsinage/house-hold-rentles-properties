from django.contrib import admin
from django.urls import path,include
from rentalapp import views


urlpatterns =[ 
    path('index3/',views.index3view,name='index3'),
    path('about/',views.aboutview,name='about'),
    path('contact/',views.contactview,name='contact'),
    path('get-a-quote/',views.getaquoteview,name='get-a-quote'),
    path('sample-inner-page/',views.sampleinnerpageview,name='sample-inner-page'),
    path('service-details/',views.servicedetailsview,name='service-details'),
    path('services/',views.servicesview,name='services'),
    path('login/',views.loginview,name='login'),
    path('logout/',views.logoutview,name='logout'),
    path('regsiter/',views.regsiterview,name='regsiter'),
    path('forms/',views.formsview,name='forms'),
    # path('table2view/',views.tableview,name='Table2view')
    path('tableview/',views.table2view,name='Table2view'),
    path('deleteproduct/<int:id>/',views.deleteproduct,name='deleteproduct'),
    path('editproduct/<int:id>/',views.editproduct,name='editproduct'),
    path('updateproduct/<int:id>/',views.updateproduct,name='updateproduct'),
    path('product/',views.productview,name='product2'),
    path('category2/',views.categoryview,name='category2'),
    path('tablecategory/',views.tablecategoryview,name='Table2category'),
    path('deletecategory/<int:id>/',views.deletecategory,name='deletecategory'),
    path('editcategory/<int:id>/',views.editcategory,name='editcategory2'),
    path('updatecategory/<int:id>/',views.updatecategory,name='updatecategory'),
]