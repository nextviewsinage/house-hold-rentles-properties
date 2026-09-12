from django.shortcuts import render, HttpResponse, redirect
from . import models
from . import forms
from ownerapp.models import product, category, confirmorder, FinalOrder
from ownerapp.forms import rentalsform, categoryform
from cart.cart import Cart
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import Http404


def index2view(request):
    data = product.objects.all()
    value = category.objects.all()
    if request.method == 'POST':
        form = rentalsform(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return HttpResponse('item added')
        else:
            print(form.errors)
    context = {'data': data, 'value': value}
    return render(request, 'index.html', context=context)


def portfoliodetailsview(request):
    return render(request, 'portfolio-details.html')


def innerpageview(request):
    return render(request, 'inner-page.html')


def blogview(request):
    return render(request, 'blog.html')


def blogsingleview(request):
    return render(request, 'blog-single.html')


def logout1view(request):
    logout(request)
    return redirect(login1view)


def login1view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(index2view)
        else:
            return HttpResponse("User does not exist")
    return render(request, 'login.html')


def regsiter1view(request):
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
                return redirect(login1view)
        else:
            return HttpResponse("Passwords do not match")
    return render(request, 'regsiter.html')


def feedbackview(request):
    form = forms.feedbackform(request.POST)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect(index2view)
        else:
            print(form.errors)
    return render(request, 'feedback.html')


@login_required(login_url='/customerapp/login1/')
def tableview(request):
    data = models.feedback.objects.all()
    context = {'data': data}
    return render(request, 'table.html', context=context)


@login_required(login_url='/customerapp/login1/')
def deletefeedback(request, id):
    data = models.feedback.objects.get(id=id)
    data.delete()
    return redirect(tableview)


@login_required(login_url='/customerapp/login1/')
def editfeedback(request, id):
    data = models.feedback.objects.get(id=id)
    context = {'data': data}
    return render(request, 'editfeedback.html', context=context)


@login_required(login_url='/customerapp/login1/')
def updatefeedback(request, id):
    data = models.feedback.objects.get(id=id)
    if request.method == "POST":
        form = forms.feedbackform(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect(tableview)
        else:
            print(form.errors)
    return render(request, 'updatefeedback.html')


@login_required(login_url='/customerapp/login1/')
def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_cart_price = 0

    for product_id, item_data in cart.items():
        try:
            product_instance = product.objects.get(pk=product_id)
        except product.DoesNotExist:
            continue

        quantity = item_data['quantity']
        subtotal = product_instance.price * quantity
        total_cart_price += subtotal

        cart_items.append({
            'product': product_instance,
            'quantity': quantity,
            'subtotal': subtotal
        })

    context = {
        'cart_items': cart_items,
        'total_cart_price': total_cart_price
    }
    return render(request, 'cart_detail.html', context)


@login_required(login_url='/customerapp/login1/')
def add_to_cart(request):
    return render(request, 'Add_to_cart.html')


def serachcategory(request, name):
    value = category.objects.all()
    data = product.objects.filter(category__name=name)
    context = {'data': data, 'value': value}
    return render(request, 'index.html', context)


@login_required(login_url='/customerapp/login1/')
def confirm_order_view(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        cart = Cart(request)
        subtotal = 0

        fnl = FinalOrder.objects.create(user=request.user, gst=0, total=0)

        for product_id, item_data in cart.cart.items():
            prod = product.objects.get(id=product_id)
            subtotal += float(item_data['price']) * float(item_data['quantity'])
            confirmorder.objects.create(
                user=request.user,
                final=fnl,
                subtotal=subtotal,
                product=prod,
                address=address,
                total=0
            )

        gst = 0.18 * subtotal
        total = subtotal + gst

        fnl.total = total
        fnl.gst = gst
        fnl.save()

        cart.clear()

        return redirect(order_successview)
    return render(request, 'confirm_order.html')


def order_successview(request):
    return render(request, 'order_success.html')


@login_required(login_url='/customerapp/login1/')
def my_orders_view(request):
    final_orders = FinalOrder.objects.filter(user=request.user)
    return render(request, 'My_order.html', {'final_orders': final_orders})


@login_required(login_url='/customerapp/login1/')
def cart_add(request, id):
    cart = Cart(request)
    try:
        pro = product.objects.get(id=id)
        cart.add(product=pro)
    except product.DoesNotExist:
        raise Http404("Product does not exist")
    return redirect(index2view)


@login_required(login_url='/customerapp/login1/')
def item_clear(request, id):
    cart = Cart(request)
    try:
        pro = product.objects.get(id=id)
        cart.remove(pro)
    except product.DoesNotExist:
        raise Http404("Product does not exist")
    return redirect(cart_detail)


@login_required(login_url='/customerapp/login1/')
def item_increment(request, id):
    cart = Cart(request)
    try:
        pro = product.objects.get(id=id)
        cart.add(product=pro)
    except product.DoesNotExist:
        raise Http404("Product does not exist")
    return redirect(cart_detail)


@login_required(login_url='/customerapp/login1/')
def item_decrement(request, id):
    cart = Cart(request)
    try:
        pro = product.objects.get(id=id)
        cart.decrement(product=pro)
    except product.DoesNotExist:
        raise Http404("Product does not exist")
    return redirect(cart_detail)


@login_required(login_url='/customerapp/login1/')
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect(cart_detail)


@login_required(login_url='/customerapp/login1/')
def generate_invoice(request, order_id):
    try:
        final_order = FinalOrder.objects.get(id=order_id, user=request.user)
    except FinalOrder.DoesNotExist:
        raise Http404("Order does not exist")
    return render(request, 'invoice.html', {'final_order': final_order})


@login_required(login_url='/customerapp/login1/')
def changepasswordview(request):
    if request.method == 'POST':
        form = forms.PassForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(index2view)
        else:
            print("error")
            print(form.errors)
    return render(request, 'changepassword.html')
