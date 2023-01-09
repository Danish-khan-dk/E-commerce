from cart.cart import Cart
from django.shortcuts import render, redirect
from .models import *
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import razorpay
from django.contrib import messages


client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRECT))


# ============== index page ===============
def index(request):
    product = Product.objects.all()
    context = {
        'product': product,
    }
    return render(request, "index.html", context)

# ================== Shop Page =================


def shop(request):
    product = Product.objects.all()
    categories = Categories.objects.all()
    filter_price = Filter_Price.objects.all()
    brands = Brands.objects.all()

    CATID = request.GET.get("categories")
    PRICE_FILTER_ID = request.GET.get("filter_price")
    BRANDS_FILTER_ID = request.GET.get("filter_brands")
    print(PRICE_FILTER_ID)
    if CATID:
        product = Product.objects.filter(categories=CATID)
    elif PRICE_FILTER_ID:
        product = Product.objects.filter(filter_Price=PRICE_FILTER_ID)
    elif BRANDS_FILTER_ID:
        product = Product.objects.filter(brands=BRANDS_FILTER_ID)
    else:
        product = Product.objects.all()

    context = {
        'product': product,
        'categories': categories,
        'filter_price': filter_price,
        'brands': brands,
    }
    return render(request, "shop.html", context)

# ================= Single Product Details ===================


def product_details(request, id):
    prod = Product.objects.filter(id=id).first

    context = {
        'prod': prod
    }
    return render(request, "single_product.html", context)


def about(request):
    return render(request, "about.html")


def contact(request):
    return render(request, "contact.html")

# ============= Register ==============


def register(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        number = request.POST['number']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        number_check = User.objects.filter(username=number).exists()
        email_check = User.objects.filter(email=number).exists()

        if number_check == True:
            messages.error(request, "Your Number Already Exists")
            return redirect("/register")

        if email_check == True:
            messages.error(request, "Your Email Already Exists")
            return redirect("/register")

        if len(number) != 10:
            messages.error(request, 'Number Should Be 10 Digit')
            return redirect("/register")

        elif password != cpassword:
            messages.error(request, "Password and confirm did'nt match")
            return redirect("/register")

        else:
            user = User.objects.create_user(
                username=number, email=email, password=cpassword)
            user.first_name = fname
            user.last_name = lname
            user.save()
            messages.success(request, "Your account successfully created")
            return redirect("/login")

    return render(request, "register.html")

# ============ Login ==================


def login(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        number = request.POST["number"]
        password = request.POST["password"]

        user = authenticate(request, username=number, password=password)
        if user is not None:
            auth_login(request, user)
            # messages.success(request,"Successfully Login")
            return redirect("/")
        else:
            messages.error(request, "Something went wrong")
            return redirect("/login")

    return render(request, "login.html")


def f1product(request):
    return render(request, "f1product.html")

# =============== Logout ======================


def logout(request):
    auth_logout(request)
    return redirect("/")

# =============== Search ==================


def search(request):
    query = request.GET.get('query')
    product = Product.objects.filter(name__icontains=query)
    context = {
        'product': product,
    }
    return render(request, "search.html", context)

# =============== COntact US ====================


def Contact_us(request):
    if request.method == "POST":
        obj = Contact_us(request.POST)
        obj.save()
    else:
        d = {"form": Contact_us}
        return render(request, "contact.html")

# ================= Cart ==================


@login_required(login_url="/login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("/")


@login_required(login_url="/login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/login")
def cart_detail(request):
    return render(request, 'cart.html')


def checkout(request):
    amount_str = request.POST.get('amount')
    amount_float = float(amount_str)
    amount = int(amount_float)
    payment = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": "1"
    })

    order_id = payment['id']
    context = {
        "order_id": order_id,
        "payment": payment
    }
    return render(request, 'checkout.html',context)


def placeorder(request):
    if request.method == "POST":
        uid = request.session.get("_auth_user_id")
        user = User.objects.get(id=uid)
        cart = request.session.get('cart')
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        pincode = request.POST.get("pincode")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        amount = request.POST.get("amount")

        order_id = request.POST.get("order_id")
        payment = request.POST.get("payment")

        print(firstname,lastname,phone,email,pincode,address)

        order = Order(
            user=user,
            firstname=firstname,
            lastname=lastname,
            address=address,
            city=city,
            state=state,
            pincode=pincode,
            phone=phone,
            email=email,
            payment_id=order_id,
            amount=amount,
        )
        order.save()
        for i in cart:
            a = (int(cart[i]['price']))
            b = cart[i]['quantity']
            total = a * b


            item = OrderItem(
                user = user,
                order=order,
                product=cart[i]['name'],
                image=cart[i]['image'],
                price=cart[i]['price'],
                total=total
            )
            item.save()

    return render(request,'placeorder.html')


@csrf_exempt
def success(request):
    return render(request,"thankyou.html")

def your_order(request):
    uid = request.session.get("_auth_user_id")
    user = User.objects.get(id=uid)

    order = OrderItem.objects.filter(user = user)
    
    context = {
        'order':order,
    }
    return render(request,"yourorder.html",context)