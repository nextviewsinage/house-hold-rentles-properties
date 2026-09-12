from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from . import models
from . import forms
from ownerapp.models import product, category, confirmorder, FinalOrder
from ownerapp.forms import rentalsform, categoryform
from cart.cart import Cart
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Wishlist, ProductReview, CustomerProfile, OrderStatus


# ===================== EXISTING VIEWS (unchanged) =====================

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
        # Create order status as Pending
        OrderStatus.objects.create(order=fnl, status='Pending')
        cart.clear()
        return redirect(order_successview)
    return render(request, 'confirm_order.html')


def order_successview(request):
    return render(request, 'order_success.html')


@login_required(login_url='/customerapp/login1/')
def my_orders_view(request):
    final_orders = FinalOrder.objects.filter(user=request.user).order_by('-id')
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


# ===================== NEW VIEWS =====================

# --- Product Detail Page ---
def product_detail_view(request, id):
    prod = get_object_or_404(product, id=id)
    related = product.objects.filter(category=prod.category).exclude(id=id)[:4]
    reviews = ProductReview.objects.filter(product=prod).order_by('-created_at')
    avg_rating = 0
    if reviews.exists():
        avg_rating = round(sum([r.rating for r in reviews]) / reviews.count(), 1)

    # Check if in wishlist
    in_wishlist = False
    if request.user.is_authenticated:
        in_wishlist = Wishlist.objects.filter(user=request.user, product=prod).exists()

    # Submit Review
    if request.method == 'POST' and request.user.is_authenticated:
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        if rating and comment:
            ProductReview.objects.update_or_create(
                user=request.user, product=prod,
                defaults={'rating': rating, 'comment': comment}
            )
            return redirect('product_detail', id=id)

    context = {
        'prod': prod,
        'related': related,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'in_wishlist': in_wishlist,
    }
    return render(request, 'product_detail.html', context)


# --- Product Search ---
def product_search_view(request):
    query = request.GET.get('q', '')
    value = category.objects.all()
    data = product.objects.filter(name__icontains=query) if query else product.objects.all()
    context = {'data': data, 'value': value, 'query': query}
    return render(request, 'index.html', context)


# --- Price Sorting ---
def price_sort_view(request):
    sort = request.GET.get('sort', 'asc')
    value = category.objects.all()
    if sort == 'desc':
        data = product.objects.all().order_by('-price')
    else:
        data = product.objects.all().order_by('price')
    context = {'data': data, 'value': value, 'sort': sort}
    return render(request, 'index.html', context)


# --- Wishlist Add/Remove ---
@login_required(login_url='/customerapp/login1/')
def wishlist_toggle(request, id):
    prod = get_object_or_404(product, id=id)
    obj, created = Wishlist.objects.get_or_create(user=request.user, product=prod)
    if not created:
        obj.delete()
    return redirect('product_detail', id=id)


@login_required(login_url='/customerapp/login1/')
def wishlist_view(request):
    items = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, 'wishlist.html', {'items': items})


# --- Order Cancel ---
@login_required(login_url='/customerapp/login1/')
def cancel_order_view(request, order_id):
    order = get_object_or_404(FinalOrder, id=order_id, user=request.user)
    status_obj, _ = OrderStatus.objects.get_or_create(order=order)
    if status_obj.status in ['Pending', 'Confirmed']:
        status_obj.status = 'Cancelled'
        status_obj.tracking_note = 'Order cancelled by customer.'
        status_obj.save()
    return redirect('My_order')


# --- Order Tracking ---
@login_required(login_url='/customerapp/login1/')
def order_tracking_view(request, order_id):
    order = get_object_or_404(FinalOrder, id=order_id, user=request.user)
    status_obj, _ = OrderStatus.objects.get_or_create(order=order, defaults={'status': 'Pending'})
    items = confirmorder.objects.filter(final=order)
    context = {
        'order': order,
        'status_obj': status_obj,
        'items': items,
    }
    return render(request, 'order_tracking.html', context)


# --- Customer Profile View ---
@login_required(login_url='/customerapp/login1/')
def customer_profile_view(request):
    profile, _ = CustomerProfile.objects.get_or_create(user=request.user)
    orders = FinalOrder.objects.filter(user=request.user).order_by('-id')
    wishlist_count = Wishlist.objects.filter(user=request.user).count()
    context = {
        'profile': profile,
        'orders': orders,
        'wishlist_count': wishlist_count,
    }
    return render(request, 'customer_profile.html', context)


# --- Edit Profile ---
@login_required(login_url='/customerapp/login1/')
def edit_profile_view(request):
    profile, _ = CustomerProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        # Update User fields
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()
        # Update Profile fields
        profile.phone = request.POST.get('phone', '')
        profile.address1 = request.POST.get('address1', '')
        profile.address2 = request.POST.get('address2', '')
        profile.address3 = request.POST.get('address3', '')
        profile.city = request.POST.get('city', '')
        profile.state = request.POST.get('state', '')
        profile.pincode = request.POST.get('pincode', '')
        if request.FILES.get('profile_pic'):
            profile.profile_pic = request.FILES['profile_pic']
        profile.save()
        return redirect('customer_profile')
    return render(request, 'edit_profile.html', {'profile': profile})
