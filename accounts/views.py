import re
from django.shortcuts import render,redirect
from django.http import HttpResponse
from matplotlib.style import context
from django.contrib import messages
from django.contrib.auth.models import Group

from django.contrib.auth import authenticate, logout,login
from .models import *
from .forms import CustomerForm, OrderForm, AdditemForm, ProductForm
from .filters import OrdrFilter
from .forms import CreateUserForm
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user,allowed_users,admin_only
from django.views.decorators.csrf import csrf_exempt


from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseBadRequest
import json
from django.http import JsonResponse
import datetime

ar=-1	

from django.http import JsonResponse
from .models import Order
@csrf_exempt
def update_order(request):
    if request.method == 'POST' and request.is_ajax():
        order_id = request.POST.get('order_id')
        delivery_agent_id = request.POST.get('delivery_agent_id')
        deliveryagent=request.user.deliveryagent
        
        try:
            order = Order.objects.get(id=order_id)
            
            # Update the order status
            order.status = 'accepted'
            order.save()

            # Assign the delivery agent to the order
            order.Deliveryagent= deliveryagent
            order.save()

            # Assuming the update was successful, return a JSON response
            return JsonResponse({'success': True})
        except Order.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Order not found'})
    else:
        return JsonResponse({'success': False})

def interface(request):
    context = {}
    return render(request, 'accounts/index.html', context)
    

@unauthenticated_user
def registerpage(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
        number = request.POST['number']
        print(number)
        door_number = request.POST['door_number']
        address = request.POST['address']
        
        if len(password) <8:
            messages.error(request,'Password is too short')
            return redirect('register')
            
        if password1 == password:
            
            try:
                user = User.objects.get(username = username)
                messages.success(request, 'Username already exists try another one')
                return redirect('register')
            except User.DoesNotExist:

                myuser = User.objects.create_user(username = username,email = email,password = password)
                myuser.number = number
                myuser.address = address
                myuser.door_number = door_number
                myuser.save()
                
                group,created = Group.objects.get_or_create(name = 'customer')
                myuser.groups.add(group)
                
                Customer.objects.create(
                    user = myuser,
                    name = myuser.username,
                    number = myuser.number,
                    email = myuser.email,
                    door_number=myuser.door_number,
                    address=myuser.address
                    
                    # phone = instance.mobile_number
                )
                
                subject = 'Thank you for using'
                message = 'Welcome to OSP! we are very proud to have you'
                from_email = settings.EMAIL_HOST_USER
                print(myuser.email)
                to_list = [myuser.email, 'sivasaiyeswanth@gmail.com']
                # send_mail(subject, message, from_email, to_list, fail_silently= True)
                
                
                    
                messages.success(request, 'Customer Account created for '+username)
                return redirect('login')
            
        else:
            messages.success(request, 'Passwords did not match')
            return redirect('register')
            
            
        
            
        
            
    context = {}
    return render(request,'accounts/register.html', context)


def register_seller(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
        number = request.POST['number']
        address = request.POST['Address']
        
        
        if password1 == password:
            
            try:
                user = User.objects.get(username = username)
                messages.success(request, 'Username already exists try another one')
                return redirect('register')
            except User.DoesNotExist:
                    
                myuser = User.objects.create_user(username = username,password = password)
                myuser.number = number
                myuser.email = email
               
                myuser.save()
                
                group,created = Group.objects.get_or_create(name = 'seller')
                myuser.groups.add(group)
                
                Seller.objects.create(
                    user = myuser,
                    name = myuser.username,
                    phone = myuser.number,
                    email = myuser.email,
                    
                    # phone = instance.mobile_number
                )
                
                
                    
                messages.success(request, 'Seller Account created for '+username)
                
                return redirect('login')
        else:
            messages.success(request, 'Passwords did not match')
            return redirect('register')
                
            
    context = {}
    return render(request,'accounts/seller.html', context)

def register_deliveryagent(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
        number = request.POST['number']
       
        
        if password1 == password:
            
            try:
                user = User.objects.get(username = username)
                messages.success(request, 'Username already exists try another one')
                return redirect('register')
            except User.DoesNotExist:
                myuser = User.objects.create_user(username = username,password = password)
                myuser.number = number
                myuser.email = email
                
                myuser.save()
                
                group,created = Group.objects.get_or_create(name='deliveryagent')
                myuser.groups.add(group)
                
                Deliveryagent.objects.create(
                    user = myuser,
                    name = myuser.username,
                    phone = myuser.number,
                    email = myuser.email,
                    
                    # phone = instance.mobile_number
                )
                
                
                    
                messages.success(request, 'Delivery Agent Account created for '+username)
                
                return redirect('login')
        else:
            messages.success(request, 'Passwords did not match')
            return redirect('register')
                
            
    context = {}
    return render(request,'accounts/deliveryagent.html', context)
def deliveryagent_home(request):
    context = {}
    return render(request, 'accounts/deliveryagenthome.html', context)
def Address(request):
    orders=Order.objects.filter(complete=False,status="confirmed")
    
    
    context = {'orders':orders}
    return render(request, 'accounts/addressal.html', context )
def MyAddress(request):
    deliveryagent=request.user.deliveryagent
    orders=Order.objects.filter(complete=False,Deliveryagent=deliveryagent)
    
    
    context = {'orders':orders}
    return render(request, 'accounts/my_orders.html', context )

    
def salary(request):
    deliveryagent=request.user.deliveryagent
    context={'deliveryagent':deliveryagent}
    return render(request,'accounts/salary.html',context)
    

def loginpage(request):
    
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username = username, password = password) 
        
        if user is not None:
            login(request,user)
            return redirect('sellerhome')
        else:
            messages.info(request,'Username or password is incorrect')
        
    context = {}
    return render(request,'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    sellers = Seller.objects.all()
    
    total_orders = orders.count()
    total_customers = customers.count()
    
    delivered = orders.filter(status = 'Delivered').count()
    pending  = orders.filter(status = 'Pending').count()
    
    
    context = {'orders' : orders, 'customers' : customers, 'sellers': sellers, 'total_orders':total_orders,'total_customers':total_customers,
               'delivered':delivered ,'pending':pending}
    return render(request, 'accounts/dashboard.html',context)



@admin_only
def seller_home(request):
    context = {}
    return render(request, 'accounts/sellerhome.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['seller'])
def seller_inventory(request):
    
    products = request.user.seller.product_set.all()
    context = {'products': products}
    return render(request, 'accounts/seller_Inventory.html', context)
def seller_additem(request):
    seller = request.user.seller

    if request.method == 'POST':
        itemname = request.POST.get('itemname')
        itemcategory = request.POST.get('itemcategory')
        itemcity = request.POST.get('itemcity')
        itemdesc = request.POST.get('itemdesc')
        itemprice = request.POST.get('itemprice')
        itemimage = request.POST.get('itemimage')

        if itemimage:
            product = Product.objects.create(
                Seller=seller,
                name=itemname,
                price=itemprice,
                category=itemcategory,
                city=itemcity,
                description=itemdesc,
                image=itemimage
            )
            

        else:
            return HttpResponseBadRequest("Missing required fields")

    context = {}
    return render(request, 'accounts/seller_Add_Item.html', context)


'''def seller_additem(request):
    
    seller=request.user.seller
    
    if request.method == 'POST':
        
        itemname = request.POST['itemname']
        itemcategory = request.POST['itemcategory']
        itemcity = request.POST['itemcity']
        itemdesc = request.POST['itemdesc']
        itemprice = request.POST['itemprice']
        itemimage = request.POST['itemimage']
        
        product = Product.objects.create()
        
        product.Seller = request.user.seller
        product.name = itemname
        product.price = itemprice
        product.category = itemcategory
        product.city = itemcity
        product.description = itemdesc
        product.image = itemimage
        
        product.save()
        
        print(product)
        
    
        
    context = {}
    return render(request, 'accounts/seller_Add_Item.html', context)
'''




@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    
    total_orders = orders.count()
    delivered = orders.filter(status = 'Delivered').count()
    pending  = orders.filter(status = 'Pending').count()
    
    
    context = {'orders' : orders, 'total_orders':total_orders,
               'delivered':delivered ,'pending':pending}
    return render(request, 'accounts/user.html',context)

@allowed_users(allowed_roles=['customer', 'manager'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance= customer)
        
        if form.is_valid():
            form.save()
            
    
    context = {'form':form}
    
    return render(request, 'accounts/account_settings.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['seller'])
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html',{'products':products})




@login_required(login_url='login')
@allowed_users(allowed_roles=['seller'])
def addprod(request):
    form = AdditemForm()
    
    if request == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sellerhome')
        
    
    context = {'form':form}
    
    return render(request, 'accounts/seller_additem2.html', context)
    
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def search(request):

    if request.method=="POST":

        searched=request.POST['searched']

        data=Product.objects.filter(name__contains=searched).order_by('-id')

        return render(request, 'accounts/search.html',{'searched':searched,'data':data})

    else:

        return render(request, 'accounts/search.html',{})

# Create your views here.
@login_required(login_url='login')
@allowed_users(allowed_roles=['seller'])
def updateOrder(request,test_id):
    
    order = Order.objects.get(id = test_id)
    form = OrderForm(instance=order)
    
    if request.method == 'POST':
        #print('Printing POST:', request.POST)
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    
    context = {'form':form}
    
    
    return render(request,'accounts/order_form.html',context)

@allowed_users(allowed_roles=['seller'])
def update_prod(request, test_id):
    
    product = Product.objects.get(id = test_id)
    form = ProductForm(instance= product)
    
    if request.method == 'POST':
        
        form = ProductForm(request.POST, instance= product)
        group = request.user.groups.all()[0].name
        if form.is_valid():
            form.save()
            
            if group == 'seller':
                return redirect('sellerhome')
            
            
            # return redirect('sellerhome')
        
    
    context = {'form':form}
    
    return render(request, 'accounts/prod_form.html', context)

def update_ord(request, test_id,test_i):
    
    order = Order.objects.get(id = test_id)
    form = OrderForm(instance= order)
    if request.method == 'POST':
        
        form = OrderForm(request.POST, instance= order)
        group = request.user.groups.all()[0].name
        if form.is_valid():
            form.save()
            
           
            return redirect('vieword',test_i)
            
            # return redirect('sellerhome')
        
    
    context = {'form':form,'test_id':test_id}
    
    return render(request, 'accounts/order_form.html', context)

    
def vieword(request,test_id):
    customer = Customer.objects.get(id = test_id)
    
    order= Order.objects.get(Customer=customer,complete=False)
    
    items=order.orderitem_set.all()
    context = {'items':items, 'order':order,'test_id':test_id}
    
    return render(request, 'accounts/order_detail.html', context)

def view_prod(request, test_id):
    
    product = Product.objects.get(id = test_id)
    
    context = {'product':product}
    
    return render(request, 'accounts/view_prod.html', context)

def seller_view(request, test_id):
    
    product = Product.objects.get(id = test_id)
    
    context = {'product':product}
    
    return render(request, 'accounts/seller_view.html', context)
        

@login_required(login_url='login')
@allowed_users(allowed_roles=['seller'])
def deleteOrder(request, test_id):
     
    order = Order.objects.get(id = test_id)
    context = {'item':order}
    
    if request.method == 'POST':
        order.delete()
        return redirect('/')
        
    return render(request,'accounts/delete.html',context)

@allowed_users(allowed_roles=['seller'])
def delete_product(request, test_id):
    
    product = Product.objects.get(id = test_id)
    group = request.user.groups.all()[0].name
    
    context = {'product':product}
    
    context = {'item':product}
    
    if request.method == 'POST':
        product.delete()
        if group == 'seller':
                return redirect('sellerhome')
        
        
        
        # return redirect('sellerhome')
    
    return render(request, 'accounts/deleteprod.html', context)


def seller_account(request):
    context = {}
    return render(request, 'accounts/selleraccount.html', context)
def delivery_account(request):
    context = {}
    return render(request, 'accounts/deliveryaccount.html', context)
    


def payment(request,  test_id):
    order = Order.objects.get(id = test_id)
    order.status="confirmed"
    order.save()
    context = {'order':order}
    return render(request, 'accounts/payment.html', context)
    
def trackorder(request):
    customer=request.user.customer
    try:
        order= Order.objects.get(Customer=customer,complete=False) 
        print(order)
        if order.status == "accepted":
           context = {'order':order}
           return render(request,'accounts/accepted.html',context)
        if order.status == "outfordelivery":
           context = {'order':order}
           return render(request,'accounts/outfordelivery.html',context)
        if order.status == "delivered":
           order.complete=True
           order.save()
           context = {'order':order}
           return render(request,'accounts/delivered.html',context)  
        else:
           messages.success(request, 'Your order is not accepted by any delivery agent!Wait for some time')
           return render(request,'accounts/buyer.html')  
    except Order.DoesNotExist:
        messages.info(request, 'There are no orders for you.')
    
    return render(request, 'accounts/buyer.html')

@allowed_users(allowed_roles=['customer'])
def buyer(request):
    context={}
    return render(request, 'accounts/buyer.html',context)


def item(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order, created = Order.objects.get_or_create(Customer=customer,complete=False,status="pending")
        items=order.orderitem_set.all()
    else:
        items=[]
        orders={'get_cart_total':0,'get_cart_items':0,'shipping':False}
    products=Product.objects.all()
    context = {'products':products}
    return render(request, 'accounts/item.html',context)

def cart(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order, created = Order.objects.get_or_create(Customer=customer,complete=False,status="pending")
        items=order.orderitem_set.all()
        
    else:
        items=[]
        orders={'get_cart_total':0,'get_cart_items':0,'shipping':False}
    print(order)
    for ite in items:
        print(ite.product.price)
    context = {'items':items, 'order':order}
    return render(request, 'accounts/cart.html',context)
def cancel(request):
    customer=request.user.customer
    if request.user.is_authenticated:
        amount=None
       # print(1000)
       # amount = request.POST.get('Amount')
       # print(amount)
        #customer.Amount=amount
        if request.method == 'POST':
             amount = request.POST.get("Amount")
        
             
        order, created = Order.objects.get_or_create(Customer=customer,complete=False,status="pending")
        items=Order.orderitem_set.all()
      
    else:
        items=[]
        
        subscriptions={'get_order_total':0,'get_order_items':0}
    context = {'items':items, 'subscription':subscription}
    
    return render(request, 'accounts/cancel.html', context)
     

def checkout(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(Customer=customer,complete=False,status="pending")
        items=order.orderitem_set.all()
    else:
        items=[]
        orders={'get_cart_total':0,'get_cart_items':0,'shipping':False}

    context = {'items':items, 'order':order}
    return render(request, 'accounts/checkout.html',context)

def myaccount(request):
    
    customer=request.user.customer
    orders = customer.order_set.all()
    
    print(orders)
    
    context = {'orders':orders}
    return render(request, 'accounts/myaccount.html', context)



def updateitem(request):
    
    data=json.loads(request.body)
    prodID=data['prodID']
    action=data['action']
    print('action:',action)
    print('prodID:',prodID)

    customer=request.user.customer
    product=Product.objects.get(id=prodID) 
    Area=request.user.customer.address
    door_number=request.user.customer.door_number
    order,created=Order.objects.get_or_create(Customer=customer,complete=False,status="pending")
    orderItem,created=OrderItem.objects.get_or_create(order=order,product=product,address=Area,door_number=door_number)
    if action=='add':
        orderItem.quantity=(orderItem.quantity+1)
    elif action=='remove':
        orderItem.quantity=(orderItem.quantity-1)
    orderItem.save()
    if orderItem.quantity<=0:
        orderItem.delete()
    
    return JsonResponse('item added',safe=False)

def processorder(request):
    transactionid=datetime.datetime.now().timestamp()
    data=json.loads(request.body)

    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(Customer=customer,complete=False)
        total=float(data['form']['total'])
        order.transactionid=transactionid

        if total==order.get_cart_total:
            order.complete=True
        order.save()
    
        if order.shipping==True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
                
            )
    else:
        print('Login to continue')
    return JsonResponse('payment done',safe=False)


