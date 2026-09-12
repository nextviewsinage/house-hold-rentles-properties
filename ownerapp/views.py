from django.shortcuts import render,HttpResponse,redirect
from . import forms
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import login,logout,authenticate
# from forms import blogform
from . import models
from cart.cart import Cart
from rentalapp.models import product
from cart.cart import Cart


def indexview(request):
    data = models.product.objects.all()
    value = models.category.objects.all()
    if request.method=='POST':
            form = forms.rentalsform(request.POST)
            if form.is_valid():
                    obj = form.save(commit=False)
                    obj.user = request.user
                    obj.save()
                    return HttpResponse('item added')
            else:
                    print(form.errors)
    context = {'data':data,'value':value,}
    return render(request,'ownerapp/index.html',context=context)		

def portfoliodetailsview(request):
        return render(request,'ownerapp/portfolio-details.html')
    
def innerpageview(request):
        return render(request,'inner-page.html')
     
def logout2view(request):
    logout(request)
    return redirect(login2view)
    
def formsview(request):
        form = forms.productform(request.POST)
        if request.method == "POST":
                if form.is_valid():
                 form.save()
                 return redirect(indexview)
        else:
                print(form.errors)       
   
        return render(request,'ownerapp/forms.html')

def login2view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect(indexview)
        else:
            return HttpResponse("user dose not exist")
    return render(request,'ownerapp/login.html')


def regsiteriew(request):

    if request.method=='POST':
       if request.POST.get('password')== request.POST.get('password1'):
        
           try:
               User.objects.get(username=request.POST.get('username'))
               return HttpResponse("already exists")
           except:
               User.objects.create_user(username=request.POST.get('username'),
                                        password=request.POST.get('password'),
                                        email=request.POST.get('email'))
               return redirect(login2view)
       else:
               return HttpResponse("password not same")
           
    return render(request,'ownerapp/regsiter.html')


def tableview(request):
    data = models.product.objects.all()
    context = {'data':data}
    return render(request,'ownerapp/table.html',context=context)

def deleteproduct(request,id):
    data = models.product.objects.get(id=id)
    data.delete()
    return redirect(tableview)

def editproduct(request,id):
    data = models.product.objects.get(id=id)
    category = models.category.objects.all()
    context = {'data':data, 'category':category}	
    return render(request,'ownerapp/editproduct.html',context=context)

def updateproduct(request,id):
    data = models.product.objects.get(id=id)
    form = forms.productform(request.POST,instance=data)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect(tableview)
        else:
            print(form.errors)   
    return render(request,'ownerapp/editproduct.html') 

from .forms import productform

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
    return render(request, 'ownerapp/product.html', {'form': form, 'category': category})


def category(request):
        data = models.category.objects.all()
        form = forms.categoryform(request.POST)
        if request.method == "POST":
                if form.is_valid():
                 form.save()
                 return redirect(indexview)
        else:
                print(form.errors)       
        context = {'data':data}
        return render(request,'ownerapp/category.html',context=context)
                

def tablecategoryview(request):
    data = models.category.objects.all()
    context = {'data':data}
    return render(request,'ownerapp/tablecategory.html',context=context)

def deletecategory(request,id):
    data = models.category.objects.get(id=id)
    data.delete()
    return redirect(tableview)

def editcategory(request,id):
    data = models.category.objects.get(id=id)
    context = {'data':data}
    return render(request,'ownerapp/editcategory.html',context=context)

def updatecategory(request,id):
    data = models.category.objects.get(id=id)
    if request.method == "POST":
        form = forms.categoryform(request.POST,instance=data)
        if form.is_valid():
            form.save()
            return redirect(tableview)
        else:
            print(form.errors)   
    return render(request,'ownerapp/updatecategory.html')
  
  
# def cart_add(request, id):
#     cart = Cart(request)
#     product = models.product.objects.get(id=id)
#     cart.add(product=product)
#     return redirect(indexview)


# def item_clear(request, id):
#     cart = Cart(request)
#     product = models.product.objects.get(id=id)
#     cart.remove(product)
#     return redirect(cart_detail)

# def item_increment(request, id):
#     cart = Cart(request)
#     product = models.product.objects.get(id=id)
#     cart.add(product=product)
#     return redirect(cart_detail)

# def item_decrement(request, id):
    cart = Cart(request)
    product = models.product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect(cart_detail)

# def cart_clear(request):
#     cart = Cart(request)
#     cart.clear()
#     return redirect(cart_detail)

# from django.shortcuts import render
# from .models import product
# from cart.cart import Cart
# from django.shortcuts import render, redirect
# from .models import product

# def cart_detail(request):
#     cart = request.session.get('cart', {})  # Retrieve cart data from session
#     cart_items = []

#     total_cart_price = 0

#     # Iterate over cart items
#     for product_id, item_data in cart.items():
#         product_instance = product.objects.get(pk=product_id)
#         quantity = item_data['quantity']
#         subtotal = product_instance.price * quantity
#         total_cart_price += subtotal

#         cart_items.append({
#             'product': product_instance,
#             'quantity': quantity,
#             'subtotal': subtotal
#         })

#     context = {
#         'cart_items': cart_items,
#         'total_cart_price': total_cart_price
#     }

#     return render(request, 'ownerapp/cart_detail.html', context)



# def add_to_cart(request):
#     return render(request, 'ownerapp/Add_to_cart.html')


# def serachcategory(request,name):
#     value = models.category.objects.all()
#     if request.method == 'POST':
#         data = models.product.objects.filter(category__name=name)
#         print(data)
#         context = {'data':data,'value':value}
#     return render(request,'ownerapp/index.html',context)


# def confirm_order_view(request):
#     if request.method == 'POST':
#         cart = Cart(request)
#         subtotal = 0 
#         x = cart.cart.values()
#         print(x)
#         y = list(x)
#         print(y)    
#         product_ids = [item['product_id'] for item in y]
#         print("product_ids",product_ids)
#         num = 0
#         for ab in cart.cart.values():
#             subtotal += float(ab['price']) * float(ab['quantity'])
#             prod = models.product.objects.get(id=num)
#             order = models.confirmorder.objects.create(user = request.user,
#                                                 subtotal = subtotal ,
#                                                 product = prod,
#                                                 address = request.POST.get('address'),
#                                                 total = 0)
#             num+=1
            
#         print(subtotal)
#         gst = 0.18 * subtotal
#         total = subtotal + gst
        
#         order.total = total
#         order.save()
        
#     return render(request,'ownerapp/confirm_order.html')


   
def changepass1wordview(request):
    if request.method == 'POST':
        form = forms.PassForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            login2view(request,user)
            return redirect(indexview)
        else:
            print("error")
            print(form.errors)
    return render(request, 'changepassword.html')