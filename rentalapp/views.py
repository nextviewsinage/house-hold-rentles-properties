from django.shortcuts import render,HttpResponse,redirect
from . import forms
from ownerapp.models import product,category
from ownerapp.forms import rentalsform,categoryform
from .forms import productform
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import login,logout,authenticate
# Create your views here.
from . import models

def index3view(request):
    if request.method=='POST':
        form = forms.rentalsform(request.POST)
        if form.is_valid():
                obj = form.save(commit=False)
                obj.user = request.user
                obj.save()
                return HttpResponse('item added')
        else:
                print(form.errors)
    return render(request,'rentalapp/index.html')

def aboutview(request):
    return render(request,'rentalapp/about.html')

def contactview(request):
    return render(request,'rentalapp/contact.html')

def getaquoteview(request):
    return render(request,'rentalapp/get-a-quote.html')

def sampleinnerpageview(request):
    return render(request,'rentalapp/sample-inner-page.html')

def servicedetailsview(request):
    return render(request,'rentalapp/service-details.html')

def servicesview(request):
    return render(request,'rentalapp/services.html')

def formsview(request):
    if request.method == "POST":
        form = forms.productform(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(index3view)
        else:
            print(form.errors)         
    return render(request,'rentalapp/forms.html')


def loginview(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect(index3view)
        else:
            return HttpResponse("user succes login")
    return render(request,'rentalapp/login.html')

def logoutview(request):
    logout(request)
    return redirect(index3view)


def regsiterview(request):
    
    if request.method=='POST':
       if request.POST.get('password')== request.POST.get('password1'):
        
           try:
               User.objects.get(username=request.POST.get('username'))
               return HttpResponse("already exists")
           except:
               User.objects.create_user(username=request.POST.get('username'),
                                        password=request.POST.get('password'),
                                        email=request.POST.get('email'))
               return redirect(loginview)
       else:
               return HttpResponse("password not same")
    return render(request,'rentalapp/regsiter.html')


def productview(request):
    cate = category.objects.all()
    if request.method == "POST":
        form = productform(request.POST, request.FILES)  # Use ProductForm instead of product
        if form.is_valid():
                obj = form.save(commit=False)
                obj.user = request.user
                obj.save()
                return redirect(index3view)
        else:
                print(form.errors)   
    else:
        form = productform()  # Create a new form instance for GET requests
    return render(request, 'rentalapp/product2.html', {'category': cate, 'form': form})

def deleteproduct(request,id):
    data = models.product.objects.get(id=id)
    data.delete()
    return redirect(table2view)

def editproduct(request,id):
    data = product.objects.get(id=id)
    cate = category.objects.all()
    context = {'data':data, 'category':category}	
    return render(request,'rentalapp/editproduct2.html',context=context)

def updateproduct(request,id):
    data = models.product.objects.get(id=id)
    form = forms.productform(request.POST,instance=data)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect(table2view)
        else:
            print(form.errors)   
    return render(request,'rentalapp/updateproduct2.html') 
  

def categoryview(request):
    data = category.objects.all()
    form = categoryform(request.POST)
    if request.method == "POST":
                if form.is_valid():
                 form.save()
                 return redirect(index3view)
    else:
                print(form.errors)       
    context = {'data':data}
    return render(request,'rentalapp/Category2.html',context=context)

def table2view(request):
    data = models.product.objects.all()
    context = {'data':data}
    return render(request,'rentalapp/Table2.html',context=context)

def tablecategoryview(request):
    data = category.objects.all()
    context = {'data':data}
    return render(request,'rentalapp/table2category.html',context=context)

def deletecategory(request,id):
    data = category.objects.get(id=id)
    data.delete()
    return redirect(table2view)

def editcategory(request,id):
    data = category.objects.get(id=id)
    context = {'data':data}
    return render(request,'rentalapp/editcategory2.html',context=context)

def updatecategory(request,id):
    data = category.objects.get(id=id)
    if request.method == "POST":
        form = categoryform(request.POST,instance=data)
        if form.is_valid():
            form.save()
            return redirect(table2view)
        else:
            print(form.errors)   
    return render(request,'rentalapp/updatecategory2.html')


