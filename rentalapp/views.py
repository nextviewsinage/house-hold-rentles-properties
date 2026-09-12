from django.shortcuts import render, HttpResponse, redirect
from . import forms
from ownerapp.models import product as owner_product, category
from ownerapp.forms import rentalsform, categoryform
from .forms import productform
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from . import models


def index3view(request):
    return render(request, 'rentalapp/index.html')


def aboutview(request):
    return render(request, 'rentalapp/about.html')


def contactview(request):
    return render(request, 'rentalapp/contact.html')


def getaquoteview(request):
    return render(request, 'rentalapp/get-a-quote.html')


def sampleinnerpageview(request):
    return render(request, 'rentalapp/sample-inner-page.html')


def servicedetailsview(request):
    return render(request, 'rentalapp/service-details.html')


def servicesview(request):
    return render(request, 'rentalapp/services.html')


def loginview(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(index3view)
        else:
            return HttpResponse("User does not exist")
    return render(request, 'rentalapp/login.html')


def logoutview(request):
    logout(request)
    return redirect(index3view)


def regsiterview(request):
    if request.method == 'POST':
        if request.POST.get('password') == request.POST.get('password1'):
            try:
                User.objects.get(username=request.POST.get('username'))
                return HttpResponse("Already exists")
            except:
                User.objects.create_user(
                    username=request.POST.get('username'),
                    password=request.POST.get('password'),
                    email=request.POST.get('email')
                )
                return redirect(loginview)
        else:
            return HttpResponse("Passwords do not match")
    return render(request, 'rentalapp/regsiter.html')


@login_required(login_url='/rentalapp/login/')
def formsview(request):
    if request.method == "POST":
        form = forms.productform(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(index3view)
        else:
            print(form.errors)
    return render(request, 'rentalapp/forms.html')


@login_required(login_url='/rentalapp/login/')
def productview(request):
    cate = category.objects.all()
    if request.method == "POST":
        form = productform(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect(index3view)
        else:
            print(form.errors)
    else:
        form = productform()
    return render(request, 'rentalapp/product2.html', {'category': cate, 'form': form})


@login_required(login_url='/rentalapp/login/')
def table2view(request):
    data = models.product.objects.all()
    context = {'data': data}
    return render(request, 'rentalapp/Table2.html', context=context)


@login_required(login_url='/rentalapp/login/')
def deleteproduct(request, id):
    data = models.product.objects.get(id=id)
    data.delete()
    return redirect(table2view)


@login_required(login_url='/rentalapp/login/')
def editproduct(request, id):
    data = models.product.objects.get(id=id)
    cate = category.objects.all()
    context = {'data': data, 'category': cate}
    return render(request, 'rentalapp/editproduct2.html', context=context)


@login_required(login_url='/rentalapp/login/')
def updateproduct(request, id):
    data = models.product.objects.get(id=id)
    if request.method == "POST":
        form = forms.productform(request.POST, request.FILES, instance=data)
        if form.is_valid():
            form.save()
            return redirect(table2view)
        else:
            print(form.errors)
    else:
        form = forms.productform(instance=data)
        return render(request, 'rentalapp/editproduct2.html', {'form': form, 'data': data})
    return render(request, 'rentalapp/updateproduct2.html')


@login_required(login_url='/rentalapp/login/')
def categoryview(request):
    data = category.objects.all()
    if request.method == "POST":
        form = categoryform(request.POST)
        if form.is_valid():
            form.save()
            return redirect(index3view)
        else:
            print(form.errors)
    else:
        form = categoryform()
    context = {'data': data, 'form': form}
    return render(request, 'rentalapp/Category2.html', context=context)


@login_required(login_url='/rentalapp/login/')
def tablecategoryview(request):
    data = category.objects.all()
    context = {'data': data}
    return render(request, 'rentalapp/table2category.html', context=context)


@login_required(login_url='/rentalapp/login/')
def deletecategory(request, id):
    data = category.objects.get(id=id)
    data.delete()
    return redirect(tablecategoryview)


@login_required(login_url='/rentalapp/login/')
def editcategory(request, id):
    data = category.objects.get(id=id)
    context = {'data': data}
    return render(request, 'rentalapp/editcategory2.html', context=context)


@login_required(login_url='/rentalapp/login/')
def updatecategory(request, id):
    data = category.objects.get(id=id)
    if request.method == "POST":
        form = categoryform(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect(tablecategoryview)
        else:
            print(form.errors)
    else:
        form = categoryform(instance=data)
        return render(request, 'rentalapp/editcategory2.html', {'form': form, 'data': data})
    return render(request, 'rentalapp/updatecategory2.html')
