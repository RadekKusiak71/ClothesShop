from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

from .models import Cart, CartItem, Product, Category,Order,Order_details,OrderItem
from .forms import NewUserForm






def Home(request):
    top_sales = Product.objects.order_by('-sales')[0:3]
    return render(request,'main/home.html',{'products':top_sales})


def Products(request):
    return render(request,'main/products.html',{})

def About(request):
    return render(request,'main/about.html',{})


def Piece(request,pk):
    product = Product.objects.get(id=pk)
    top_sales = Product.objects.order_by('-sales')
    return render(request,'main/piece.html',{'product':product,'top_sales':top_sales})

@login_required
def Orders_list(request):
    orders = Order.objects.filter(owner=request.user)
    counter = 0
    for i in orders:
        counter +=1
    return render(request,'main/orders.html',{'orders':orders,'counter':counter})

@login_required
def Order_details_request(request,order_id):
    order = Order.objects.get(id=order_id)
    details = Order_details.objects.get(order=order)
    items = OrderItem.objects.filter(order=order)
    return render(request,'main/order-details.html',{'details':details,'order':order,'items':items})

def Categories(request,id):
    if id == 1:
        category = Category.objects.get(name='Tee')
        products = Product.objects.filter(category=category)
    elif id == 2:
        category = Category.objects.get(name='Hoodie')
        products = Product.objects.filter(category=category)
    else:
        messages.error(request,'There was a problem, please try again later')
        return redirect('products-page')
    
    return render(request,'main/products-category.html',{'category':category,'products':products})


@login_required
def add_to_cart(request,product_id):
    cart = Cart.objects.get_or_create(owner=request.user)[0]
    product = Product.objects.get(id=product_id)
    CartItem.objects.create(product=product,cart=cart)
    messages.success(request, f"{product.name} has been added to your cart.")
    return redirect(reverse('piece-page',args=[product_id]))

def add_to_cart_anonymous(request, product_id):
    session_key = request.session.session_key
    if not session_key:
        request.session.save()
        session_key = request.session.session_key
    cart = Cart.objects.get_or_create(session_key=session_key)[0]
    product = Product.objects.get(id=product_id)
    CartItem.objects.create(product=product, cart=cart)
    return redirect(reverse('piece-page',args=[product_id]))


def Cart_page(request):
    try:
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(owner=request.user)
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.save()
                session_key = request.session.session_key
            cart, created = Cart.objects.get_or_create(session_key=session_key)

        products = CartItem.objects.filter(cart=cart)

        price = sum(item.product.price for item in products)
        
        if not products:
            cart.delete()
            cart_id = 0
        else:
            cart_id = cart.id

        context = {'products': products, 'price': price, 'cart_id': cart_id}

    except Cart.DoesNotExist:
        context = {'cart_id': 0}

    return render(request, 'main/cart.html', context)


    


def item_remove(request,product_id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            cart = Cart.objects.get(owner = request.user)
            products = CartItem.objects.filter(cart=cart)           
            for i in products:
                if i.id == product_id:
                    i.delete()
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.save()
                session_key = request.session.session_key
            cart = Cart.objects.get(session_key = session_key)
            products = CartItem.objects.filter(cart=cart)
            for i in products:
                if i.id == product_id:
                    i.delete()
                    
    return redirect('cart-page')


def order_creation(request, cart_id):
    try:
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        if not firstname or not lastname or not email or not phone or not address:
            error_msg = 'Please fill in all required fields'
            return render(request, 'main/cart.html', {'error_msg': error_msg})
        if request.method == 'POST':
            if request.user.is_authenticated:
                try:
                    cart = Cart.objects.get(id=cart_id, owner=request.user)
                except Cart.DoesNotExist:
                    return HttpResponse('Your cart is empty...')
            else:
                session_key = request.session.session_key
                if not session_key:
                    request.session.save()
                    session_key = request.session.session_key
                try:
                    cart = Cart.objects.get(session_key=session_key)
                except Cart.DoesNotExist:
                    return HttpResponse('Your cart is empty...')

            products = CartItem.objects.filter(cart=cart)

            if not products:
                return HttpResponse('Your cart is empty...')

            order = Order.objects.create(owner=request.user if request.user.is_authenticated else None, session_key=session_key if not request.user.is_authenticated else None)
            Order_details.objects.create(first_name=firstname, last_name=lastname, email=email, address=address, order=order)
            product_list = []
            price_checkout = 0
            for product in products:
                sales = Product.objects.get(name=product)
                sales.sales += 1
                price_checkout += sales.price
                print(price_checkout)
                sales.save()
                OrderItem.objects.create(product=product.product, order=order)
                product_list.append(sales.name)
                product.delete()
                
            message_email = f'NARCISSIST ORDER:\nPERSONAL DATA: {firstname} - {lastname} | PHONE: {phone} | DELIVERY ADDRESS : {address}\nPRODUCTS: {product_list}\nPrice:{price_checkout}$'
            
            send_mail(
            f'ORDER {order.id}',
            message_email,
            'TYPE IN YOU EMAIL',
            [email],
            fail_silently=False,
            )

            return redirect('home-page')

        else:
            pass
    except:
        return HttpResponse('Enter your data')

def order_cancel(request,order_id):
    if request.method == 'POST':
        user = request.user
        send_mail(
            f'ORDER {order_id}',
            f'You have cancelled your order: {order_id}',
            'TYPE IN YOUR EMAIL',
            [user.email],
            fail_silently=False,
        )
        order = Order.objects.get(id=order_id)
        order.delete()
    return redirect('orders-page')

def Register_request(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Registration Successfull')
            return redirect('login-page')
        messages.error(request,'Try again later...')
    form = NewUserForm()
    return render(request,'main/register.html',{'register_form':form})

def Login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request,f'Hello, {username}.')
                return redirect('home-page')
            else:
                messages.error(request,'Try again...')
        else:
            messages.error(request,'Try again...')
    form = AuthenticationForm()
    return render(request,'main/login.html',{'login_form':form})

@login_required
def Logout_req(request):
    logout(request)
    messages.info(request, "You have successfully logged out.") 
    return redirect("home-page")


