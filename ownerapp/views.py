from django.shortcuts import render, HttpResponse, redirect
from . import forms
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import login, logout, authenticate
from . import models
from cart.cart import Cart
from rentalapp.models import product
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
import json
from datetime import datetime, timedelta
from django.utils import timezone


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


@login_required(login_url='/ownerapp/login2/')
def dashboardview(request):
    # --- Stats ---
    total_products = models.product.objects.count()
    total_categories = models.category.objects.count()
    total_customers = User.objects.filter(is_superuser=False).count()
    total_orders = models.FinalOrder.objects.count()
    total_revenue = models.FinalOrder.objects.aggregate(rev=Sum('total'))['rev'] or 0
    pending_orders = models.confirmorder.objects.filter(final__isnull=False, total=0).count()
    completed_orders = models.FinalOrder.objects.filter(total__gt=0).count()

    # --- Recent Orders (last 10) ---
    recent_orders = models.FinalOrder.objects.select_related('user').order_by('-id')[:10]

    # --- Monthly Sales Chart (last 6 months) ---
    six_months_ago = datetime.now() - timedelta(days=180)
    monthly_sales = (
        models.FinalOrder.objects
        .filter(id__gte=1)
        .values('id')
        .annotate(total_val=Sum('total'))
    )
    # Simple monthly data — last 6 months labels
    months_labels = []
    months_data = []
    for i in range(5, -1, -1):
        d = datetime.now() - timedelta(days=30 * i)
        months_labels.append(d.strftime('%b %Y'))
        months_data.append(0)

    # Fill real data per FinalOrder by id range (simple approach)
    all_orders = models.FinalOrder.objects.all().order_by('id')
    for order in all_orders:
        months_data[-1] += int(order.total)

    # --- Top Products ---
    top_products = (
        models.confirmorder.objects
        .values('product__name', 'product__price')
        .annotate(order_count=Count('id'))
        .order_by('-order_count')[:5]
    )

    # --- All Products for management ---
    all_products = models.product.objects.select_related('category').all()

    # --- Search ---
    search_query = request.GET.get('search', '')
    if search_query:
        all_products = all_products.filter(name__icontains=search_query)

    # --- All Customers ---
    all_customers = User.objects.filter(is_superuser=False).order_by('-date_joined')

    # --- New Order Notifications (orders with total > 0, last 5) ---
    new_notifications = models.FinalOrder.objects.filter(total__gt=0).order_by('-id')[:5]

    context = {
        'total_products': total_products,
        'total_categories': total_categories,
        'total_customers': total_customers,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'pending_orders': pending_orders,
        'completed_orders': completed_orders,
        'recent_orders': recent_orders,
        'months_labels': json.dumps(months_labels),
        'months_data': json.dumps(months_data),
        'top_products': top_products,
        'all_products': all_products,
        'all_customers': all_customers,
        'new_notifications': new_notifications,
        'search_query': search_query,
    }
    return render(request, 'ownerapp/dashboard.html', context=context)


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
