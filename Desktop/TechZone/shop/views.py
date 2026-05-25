from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
import json

from .models import Category, Product, Comment, Order, OrderProduct


# ── helpers ──────────────────────────────────────────────────────────────────
def get_cart(request):
    return request.session.get('cart', {})

def save_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True

def cart_total(cart, products_dict):
    total = 0
    for pid, qty in cart.items():
        p = products_dict.get(int(pid))
        if p:
            total += float(p.price) * qty
    return total


# ── views ─────────────────────────────────────────────────────────────────────
def index(request):
    categories = Category.objects.all()
    products = Product.objects.all().order_by('-id')   # Newest first

    # Category filter
    cat_slug = request.GET.get('category', '')
    if cat_slug:
        products = products.filter(category__slug=cat_slug)

    # Search
    q = request.GET.get('q', '')
    if q:
        products = products.filter(Q(name__icontains=q) | Q(brand__icontains=q))

    # Price sort
    sort = request.GET.get('sort', '')
    if sort == 'asc':
        products = products.order_by('price')
    elif sort == 'desc':
        products = products.order_by('-price')

    context = {
        'categories': categories,
        'products': products,
        'current_cat': cat_slug,
        'current_sort': sort,
        'q': q,
        'cart_count': sum(get_cart(request).values()),
    }
    return render(request, 'shop/index.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    comments = Comment.objects.filter(product=product).order_by('-time')

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "Izoh qoldirish uchun tizimga kiring!")
            return redirect('login')
        text = request.POST.get('text', '').strip()
        rate = int(request.POST.get('rate', 5))
        if text:
            Comment.objects.create(
                text=text, rate=rate,
                product=product, user=request.user
            )
            messages.success(request, "Izohingiz qo'shildi!")
        return redirect('product_detail', slug=slug)

    specs_list = [s.strip() for s in (product.specs or '').split('|') if s.strip()]
    context = {
        'product': product,
        'comments': comments,
        'specs_list': specs_list,
        'cart_count': sum(get_cart(request).values()),
    }
    return render(request, 'shop/detail.html', context)


# ── Cart ──────────────────────────────────────────────────────────────────────
def cart_add(request, product_id):
    cart = get_cart(request)
    pid = str(product_id)
    cart[pid] = cart.get(pid, 0) + 1
    save_cart(request, cart)
    product = get_object_or_404(Product, pk=product_id)
    messages.success(request, f"'{product.name}' savatga qo'shildi!")
    return redirect(request.META.get('HTTP_REFERER', 'index'))

def cart_remove(request, product_id):
    cart = get_cart(request)
    pid = str(product_id)
    if pid in cart:
        del cart[pid]
    save_cart(request, cart)
    return redirect('cart')

def cart_update(request, product_id):
    cart = get_cart(request)
    pid = str(product_id)
    qty = int(request.POST.get('qty', 1))
    if qty > 0:
        cart[pid] = qty
    else:
        cart.pop(pid, None)
    save_cart(request, cart)
    return redirect('cart')

def cart_view(request):
    cart = get_cart(request)
    products_in_cart = []
    total = 0
    for pid, qty in cart.items():
        try:
            p = Product.objects.get(pk=int(pid))
            subtotal = float(p.price) * qty
            total += subtotal
            products_in_cart.append({'product': p, 'qty': qty, 'subtotal': subtotal})
        except Product.DoesNotExist:
            pass
    context = {
        'cart_items': products_in_cart,
        'total': total,
        'cart_count': sum(cart.values()),
    }
    return render(request, 'shop/cart.html', context)


# ── Checkout & Stripe ─────────────────────────────────────────────────────────
@login_required(login_url='login')
def checkout(request):
    cart = get_cart(request)
    if not cart:
        return redirect('cart')

    cart_items = []
    total = 0
    for pid, qty in cart.items():
        try:
            p = Product.objects.get(pk=int(pid))
            subtotal = float(p.price) * qty
            total += subtotal
            cart_items.append({'product': p, 'qty': qty, 'subtotal': subtotal})
        except Product.DoesNotExist:
            pass

    # Stripe public key (test)
    stripe_public_key = "pk_test_51OXXXXTestKeyXXXXXXXXXXXXXXXXXXXXXXXXXX"

    if request.method == 'POST':
        payment_type = request.POST.get('payment_type', 'card')
        address = request.POST.get('address', '')

        # Create order
        order = Order.objects.create(
            user=request.user,
            payment_type=payment_type,
            address=address,
            total=total
        )
        for item in cart_items:
            OrderProduct.objects.create(
                order=order,
                product=item['product'],
                quantity=item['qty'],
                price=item['product'].price
            )

        # Clear cart
        save_cart(request, {})
        messages.success(request, f"Buyurtmangiz #{order.pk} qabul qilindi! Tez orada siz bilan bog'lanamiz.")
        return redirect('order_success', order_id=order.pk)

    context = {
        'cart_items': cart_items,
        'total': total,
        'cart_count': 0,
        'stripe_public_key': stripe_public_key,
    }
    return render(request, 'shop/checkout.html', context)


def order_success(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'shop/order_success.html', {'order': order, 'cart_count': 0})


# context_processor to pass categories & cart_count to all templates
def global_context(request):
    from .models import Category
    cart = get_cart(request)
    return {
        'categories': Category.objects.all(),
        'cart_count': sum(cart.values()),
    }
