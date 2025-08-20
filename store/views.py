from django.shortcuts import render,get_object_or_404,redirect
from .models import Product,Order, OrderItem , BirthdayClient
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import RegisterForm
from .models import Type
import requests
from django.conf import settings
from django.http import HttpResponse
from datetime import date
from django.http import HttpResponse
from django.core.management import call_command
call_command("makemigrations")
call_command("migrate")


def home(request):
    return render(request , 'store/home.html')

def products_list(request):
    products = Product.objects.all()
    return render(request ,  'store/product_list.html' ,{'products':products})

def product_detail(request , pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})


def add_to_cart(request, pk):
    cart = request.session.get('cart', {})
    cart[str(pk)] = cart.get(str(pk), 0) + 1
    request.session['cart'] = cart
    print("КОРЗИНА:", request.session.get('cart'))

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return HttpResponse(status=200)

    products = Product.objects.all()
    return redirect(request.META.get('HTTP_REFERER', 'products_list'))


def cart_view(request):
    cart = request.session.get('cart', {})
    items = []
    total_price = 0

    print("КОРЗИНА:", cart)

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=int(product_id))  
        item_total = product.calculated_price * quantity
        total_price += item_total

        items.append({
            'product': product,
            'quantity': quantity,
            'item_total': item_total
        })

    context = {
        'items': items,
        'total_price': total_price
    }
    print("=== CART PAGE LOADED ===")
    from django.template.loader import get_template

    return render(request, 'store/cart.html', context)

def remove_from_cart(request, pk):
    cart = request.session.get('cart', {})
    pk_str = str(pk)

    if pk_str in cart:
        if cart[pk_str]>1:
            cart[pk_str]-=1
        else:
            del cart[pk_str]
    request.session['cart'] = cart
    return redirect('cart')

def increase(request, pk):
    cart = request.session.get('cart', {})
    pk_str = str(pk)

    if pk_str in cart:
        cart[pk_str] +=1
    request.session['cart'] = cart
    return redirect('cart')


@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('products_list')

    items = []
    total_price = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=int(product_id))
        item_total = product.calculated_price * quantity
        total_price += item_total

        items.append({
            'product': product,
            'quantity': quantity,
            'item_total': item_total
        })

    if request.method == 'POST':
        name = request.POST.get('full_name')
        phone = request.POST.get('phone_number')
        payment = request.POST.get('payment_method')

        # Создаём заказ
        order = Order.objects.create(
            user=request.user,
            full_name=name,
            phone_number=phone,
            payment_method=payment,
            total_price=total_price,
            status='Pending'
        )

        # Создаём позиции заказа
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price_at_purchase=item['product'].calculated_price
            )

       
        send_whatsapp_message(request, name, phone, items, total_price, payment)

        request.session['cart'] = {}
        return redirect('order_success')

    return render(request, 'store/checkout.html', {
        'items': items,
        'total_price': total_price
    })

def order_success(request):
    return render(request, 'store/order_success.html')


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)  
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("products_list")
    else:
        form = RegisterForm()  
    return render(request, 'store/register.html', {'form': form})

def type_products(request , type_id):
    type  = get_object_or_404(type , pk = type_id)
    products = Product.objects.filter(type = type)
    return render(request, 'store/category_products.html', {
        'type': type,
        'products': products
    })


def products_by_type(request, type_id):
    selected_type = get_object_or_404(Type, pk = type_id)
    products = Product.objects.filter(type = selected_type)
    return render(request, 'store/products_by_type.html', {
        'selected_type':selected_type,
        'products':products,
    })
    
def send_whatsapp_message(request, name, phone, items, total_price, payment):
    instance_id = "instance125773"
    token = "iikr53bc9sfebgdq"
    to = "+77017707593"

    for item in items:
        product = item['product']

        text = f"""💎 Новый заказ в KENZHE.GOLD

👤 Имя: {name}
📞 Телефон: {phone}
📦 Товар: {product.name}
💰 Цена: {product.calculated_price} ₸ x {item['quantity']}
🧮 Сумма: {item['item_total']} ₸
💳 Оплата: {payment}

Итого: {total_price} ₸"""

        response = requests.post(
            f"https://api.ultramsg.com/{instance_id}/messages/chat",
            data={
                "token": token,
                "to": to,
                "body": text
            }
        )

        print("WHATSAPP:", response.status_code, response.text)

