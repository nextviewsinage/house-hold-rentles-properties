from django.shortcuts import render, HttpResponse, redirect
from . import forms
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import login, logout, authenticate
from . import models
from cart.cart import Cart
from rentalapp.models import product
from django.contrib.auth.decorators import login_required


def indexview(request):
    data = models.product.objects.all()
    value = models.category.objects.all()
    if request.method == 'POST':
        form = forms.rentalsform(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return HttpResponse('item added')
        else:
            print(form.errors)
    context = {'data': data, 'value': value}
    return render(request, 'ownerapp/index.html', context=context)


def portfoliodetailsview(request):
    return render(request, 'ownerapp/portfolio-details.html')


def innerpageview(request):
    return render(request, 'inner-page.html')


def logout2view(request):
    logout(request)
    return redirect(login2view)


def login2view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(indexview)
        else:
            return HttpResponse("User does not exist")
    return render(request, 'ownerapp/login.html')


def regsiteriew(request):
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
                return redirect(login2view)
        else:
            return HttpResponse("Passwords do not match")
    return render(request, 'ownerapp/regsiter.html')


@login_required(login_url='/ownerapp/login2/')
def formsview(request):
    form = forms.productform(request.POST)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect(indexview)
        else:
            print(form.errors)
    return render(request, 'ownerapp/forms.html')


@login_required(login_url='/ownerapp/login2/')
def tableview(request):
    data = models.product.objects.all()
    context = {'data': data}
    return render(request, 'ownerapp/table.html', context=context)


@login_required(login_url='/ownerapp/login2/')
def deleteproduct(request, id):
    data = models.product.objects.get(id=id)
    data.delete()
    return redirect(tableview)


@login_required(login_url='/ownerapp/login2/')
def editproduct(request, id):
    data = models.product.objects.get(id=id)
    category = models.category.objects.all()
    context = {'data': data, 'category': category}
    return render(request, 'ownerapp/editproduct.html', context=context)


@login_required(login_url='/ownerapp/login2/')
def updateproduct(request, id):
    data = models.product.objects.get(id=id)
    if request.method == "POST":
        form = forms.productform(request.POST, request.FILES, instance=data)
        if form.is_valid():
            form.save()
            return redirect(tableview)
        else:
            print(form.errors)
    else:
        form = forms.productform(instance=data)
        category = models.category.objects.all()
        return render(request, 'ownerapp/editproduct.html', {'form': form, 'data': data, 'category': category})
    return render(request, 'ownerapp/editproduct.html', {'data': data})


from .forms import productform


@login_required(login_url='/ownerapp/login2/')
def productview(request):
    category = models.category.objects.all()
    form = productform(request.POST, request.FILES)
    if request.method == "POST":
        form = productform(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect(indexview)
        else:
            print(form.errors)
    else:
        form = productform()
    return render(request, 'ownerapp/product.html', {'form': form, 'category': category})


@login_required(login_url='/ownerapp/login2/')
def category(request):
    data = models.category.objects.all()
    form = forms.categoryform(request.POST)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect(indexview)
        else:
            print(form.errors)
    context = {'data': data}
    return render(request, 'ownerapp/category.html', context=context)


@login_required(login_url='/ownerapp/login2/')
def tablecategoryview(request):
    data = models.category.objects.all()
    context = {'data': data}
    return render(request, 'ownerapp/tablecategory.html', context=context)


@login_required(login_url='/ownerapp/login2/')
def deletecategory(request, id):
    data = models.category.objects.get(id=id)
    data.delete()
    return redirect(tablecategoryview)


@login_required(login_url='/ownerapp/login2/')
def editcategory(request, id):
    data = models.category.objects.get(id=id)
    context = {'data': data}
    return render(request, 'ownerapp/editcategory.html', context=context)


@login_required(login_url='/ownerapp/login2/')
def updatecategory(request, id):
    data = models.category.objects.get(id=id)
    if request.method == "POST":
        form = forms.categoryform(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect(tablecategoryview)
        else:
            print(form.errors)
    else:
        form = forms.categoryform(instance=data)
        return render(request, 'ownerapp/editcategory.html', {'form': form, 'data': data})
    return render(request, 'ownerapp/updatecategory.html')


@login_required(login_url='/ownerapp/login2/')
def changepass1wordview(request):
    if request.method == 'POST':
        form = forms.PassForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(indexview)
        else:
            print("error")
            print(form.errors)
    return render(request, 'changepassword.html')
