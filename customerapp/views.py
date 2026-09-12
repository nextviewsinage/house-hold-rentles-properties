from django.shortcuts import render,HttpResponse,redirect
from . import models
from . import forms
from ownerapp.models import product,category,confirmorder,FinalOrder
from ownerapp.forms import rentalsform,categoryform
from cart.cart import Cart
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
# Create your views here.


def index2view(request):
    data = product.objects.all()
    value = category.objects.all()
    if request.method=='POST':
            form = rentalsform(request.POST)
            if form.is_valid():
                    obj = form.save(commit=False)
                    obj.user = request.user
                    obj.save()
                    return HttpResponse('item added')
            else:
                    print(form.errors)
    context = {'data':data,'value':value,}
    return render(request,'index.html',context=context)		

def portfoliodetailsview(request):
        return render(request,'portfolio-details.html')
    
def innerpageview(request):
        return render(request,'inner-page.html')
    
def blogview(request):
        return render(request,'blog.html')
    
def blogsingleview(request):
        return render(request,'blog-single.html')
    
def logout1view(request):
    logout(request)
    return redirect(login1view)


def login1view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            login(request,user)
            return redirect(index2view)
        else:
            return HttpResponse("user dose not exist")
    return render(request,'login.html')


def regsiter1view(request):

    if request.method=='POST':
       if request.POST.get('password')== request.POST.get('password1'):
        
           try:
               User.objects.get(username=request.POST.get('username'))
               return HttpResponse("already exists")
           except:
               User.objects.create_user(username=request.POST.get('username'),
                                        password=request.POST.get('password'),
                                        email=request.POST.get('email'))
               return redirect(login1view)
       else:
               return HttpResponse("password not same")
           
    return render(request,'regsiter.html')


def feedbackview(request):
        form = forms.feedbackform(request.POST)
        if request.method == "POST":
                if form.is_valid():
                 form.save()
                 return redirect(index2view)
        else:
                print(form.errors)     
        return render(request,'feedback.html')
    

def tableview(request):
    data = models.feedback.objects.all()
    context = {'data':data}
    return render(request,'table.html',context=context)

def deletefeedback(request,id):
    data = models.feedback.objects.get(id=id)
    data.delete()
    return redirect(tableview)

def editfeedback(request,id):
    data = models.feedback.objects.get(id=id)
    context = {'data':data}
    return render(request,'editfeedback.html',context=context)

def updatefeedback(request,id):
    data = models.feedback.objects.get(id=id)
    if request.method == "POST":
        form = forms.feedbackform(request.POST,instance=data)
        if form.is_valid():
            form.save()
            return redirect(tableview)
        else:
            print(form.errors)   
    return render(request,'updatefeedback.html')  

def cart_detail(request):
    cart = request.session.get('cart', {})  
    cart_items = []
    total_cart_price = 0

    for product_id, item_data in cart.items():
        try:
            product_instance = product.objects.get(pk=product_id)
        except product.DoesNotExist:
            # Handle the case where the product doesn't exist
            continue  # Skip this product and continue with the loop

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

def add_to_cart(request):
    return render(request, 'Add_to_cart.html')


def serachcategory(request,name):
    value = category.objects.all()
    if request.method == 'POST':
        data = product.objects.filter(category__name=name)
        print(data)
        context = {'data':data,'value':value}
    return render(request,'index.html',context)


def confirm_order_view(request):
    if request.method == 'POST':
        address=request.POST.get('address')
        cart = Cart(request)
        subtotal = 0
        product_ids = [item['product_id'] for item in cart.cart.values()]
        
        fnl = FinalOrder.objects.create(user=request.user,gst=0,total=0)
        
        for product_id, item_data in cart.cart.items():
            prod = product.objects.get(id=product_id)
            subtotal += float(item_data['price']) * float(item_data['quantity'])  
            confirmorder.objects.create(user=request.user,
                                        final=fnl,
                                        subtotal=subtotal,
                                        product=prod,
                                        address=address,
                                        total=0)
        
        gst = 0.18 * subtotal
        total = subtotal + gst
        
        fnl.total = total
        fnl.gst = gst
        fnl.save()
        
        return redirect(order_successview)
    return render(request,'confirm_order.html')


# def tablecategoryview(request):
#     data = category.objects.all()
#     context = {'data':data}
#     return render(request,'tablecategory.html',context=context)

# def deletecategory(request,id):
#     data = category.objects.get(id=id)
#     data.delete()
#     return redirect(tableview)

# def editcategory(request,id):
#     data = category.objects.get(id=id)
#     context = {'data':data}
#     return render(request,'editcategory.html',context=context)

# def updatecategory(request,id):
#     data = category.objects.get(id=id)
#     if request.method == "POST":
#         form = forms.categoryform(request.POST,instance=data)
#         if form.is_valid():
#             form.save()
#             return redirect(tableview)
#         else:
#             print(form.errors)   
#     return render(request,'updatecategory.html')

# def category(request):
#         data = category.objects.all()
#         form = categoryform(request.POST)
#         if request.method == "POST":
#                 if form.is_valid():
#                  form.save()
#                  return redirect(index2view)
#         else:
#                 print(form.errors)       
#         context = {'data':data}
#         return render(request,'category.html',context=context)
    
from django.http import Http404

def cart_add(request, id):
    cart = Cart(request)
    try:
        pro = product.objects.get(id=id)
        cart.add(product=pro)
    except product.DoesNotExist:
        raise Http404("Product does not exist")
    return redirect(index2view)

# Similarly, modify other functions accordingly...

from django.http import Http404

def item_clear(request, id):
    cart = Cart(request)
    try:
        pro = product.objects.get(id=id)
        cart.remove(pro)
    except product.DoesNotExist:
        raise Http404("Product does not exist")
    return redirect(cart_detail)

def item_increment(request, id):
    cart = Cart(request)
    try:
        pro = product.objects.get(id=id)
        cart.add(product=pro)
    except product.DoesNotExist:
        raise Http404("Product does not exist")
    return redirect(cart_detail)

def item_decrement(request, id):
    cart = Cart(request)
    try:
        pro = product.objects.get(id=id)
        cart.decrement(product=pro)
    except product.DoesNotExist:
        raise Http404("Product does not exist")
    return redirect(cart_detail)

def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect(cart_detail)
from django.http import Http404

def generate_invoice(request, order_id):
    try:
        final_order = FinalOrder.objects.get(id=order_id)
    except FinalOrder.DoesNotExist:
        raise Http404("Order does not exist")
    
    print(final_order)  # For debugging purposes
    return render(request, 'invoice.html', {'final_order': final_order})


def order_successview(request):
    return render(request, 'order_success.html')

def my_orders_view(request):
    final_orders = FinalOrder.objects.filter()
    print(final_orders)  # Add this line to print final_orders to console for debugging
    return render(request, 'My_order.html', {'final_orders': final_orders})

    
def changepasswordview(request):
    if request.method == 'POST':
        form = forms.PassForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect(index2view)
        else:
            print("error")
            print(form.errors)
    return render(request, 'changepassword.html')



