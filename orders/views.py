from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from products.models import Product, SKU
from .models import Cart, CartItem
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from accounts.models import Address
from accounts.forms import AddressForm
from .models import Cart, CartItem, Order, OrderItem
from delivery.models import Shipment
import json

def _get_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_id = request.session.get('cart_session_id')
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
            request.session['cart_session_id'] = session_id
        cart, created = Cart.objects.get_or_create(session_id=session_id)
    return cart

@login_required
def checkout(request):
    cart = _get_cart(request)
    if cart.total_items == 0:
        return redirect('orders:view_cart')
        
    addresses = Address.objects.filter(user=request.user)
    address_form = AddressForm()
    return render(request, 'orders/checkout.html', {'cart': cart, 'addresses': addresses, 'address_form': address_form})

@login_required
@require_POST
def place_order(request):
    cart = _get_cart(request)
    if cart.total_items == 0:
        return redirect('orders:view_cart')

    address_id = request.POST.get('address')
    payment_method = request.POST.get('payment_method', 'RAZORPAY')
    
    if not address_id:
        # Handle error: no address selected
        return redirect('orders:checkout')
        
    address = get_object_or_404(Address, pk=address_id, user=request.user)
    address_str = f"{address.full_name}, {address.street_address}, {address.city}, {address.state} - {address.postal_code}, {address.country}. Phone: {address.phone_number}"

    # Create Order
    order = Order.objects.create(
        user=request.user,
        shipping_address=address_str,
        total_amount=cart.total_price,
        payment_method=payment_method,
        status=Order.Status.PENDING
    )

    # Create Order Items and Shipments
    # Group items by seller for shipments
    items_by_seller = {}
    
    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=item.product,
            sku=item.sku,
            quantity=item.quantity,
            price=item.total_price / item.quantity # Unit price paid
        )
        
        seller = item.product.seller
        if seller not in items_by_seller:
            items_by_seller[seller] = []
        items_by_seller[seller].append(item)

    # Create Shipments
    for seller, items in items_by_seller.items():
        Shipment.objects.create(
            order=order,
            seller=seller,
            status=Shipment.Status.PENDING
        )

    # Clear Cart
    cart.items.all().delete()
    
    # Redirect based on payment method
    if payment_method == 'COD':
        # For COD, mark as confirmed and redirect to success
        order.status = Order.Status.PAID  # Or create a new status like CONFIRMED
        order.save()
        order.shipments.update(status=Shipment.Status.READY_TO_SHIP)
        return redirect('orders:order_success')
    else:
        # Redirect to Payment (Razorpay)
        return redirect('orders:payment', order_id=order.id)

import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

@login_required
def payment(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    
    # Initialize Razorpay Client
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    
    # Create Razorpay Order
    razorpay_order_data = {
        'amount': int(order.total_amount * 100), # Amount in paise
        'currency': 'INR',
        'receipt': f'order_{order.id}',
        'payment_capture': '1'
    }
    
    try:
        razorpay_order = client.order.create(data=razorpay_order_data)
        order.payment_id = razorpay_order['id']
        order.save()
        
        context = {
            'order': order,
            'razorpay_order_id': razorpay_order['id'],
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            'amount': int(order.total_amount * 100),
            'currency': 'INR',
            'callback_url': request.build_absolute_uri('/orders/payment/verify/'),
        }
        return render(request, 'orders/payment.html', context)
    except Exception as e:
        # Handle error (e.g. log it, show message)
        return render(request, 'orders/payment.html', {'order': order, 'error': str(e)})

@csrf_exempt
def verify_payment(request):
    if request.method == "POST":
        try:
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            data = request.POST
            
            params_dict = {
                'razorpay_order_id': data['razorpay_order_id'],
                'razorpay_payment_id': data['razorpay_payment_id'],
                'razorpay_signature': data['razorpay_signature']
            }
            
            # Verify Signature
            client.utility.verify_payment_signature(params_dict)
            
            # Update Order Status
            order = Order.objects.get(payment_id=data['razorpay_order_id'])
            order.status = Order.Status.PAID
            order.save()
            
            # Update Shipments to READY_TO_SHIP
            order.shipments.update(status=Shipment.Status.READY_TO_SHIP)
            
            return redirect('orders:order_success')
        except:
            return redirect('orders:order_failed')
    return redirect('core:home')

@login_required
def order_success(request):
    return render(request, 'orders/success.html')

@login_required
def order_failed(request):
    return render(request, 'orders/failed.html')

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    total_spent = orders.aggregate(total=Sum('total_amount'))['total'] or 0
    return render(request, 'orders/order_history.html', {'orders': orders, 'total_spent': total_spent})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

from django.http import JsonResponse

@require_POST
def add_to_cart(request, product_id):
    cart = _get_cart(request)
    product = get_object_or_404(Product, pk=product_id)
    
    sku_id = request.POST.get('sku')
    quantity = int(request.POST.get('quantity', 1))
    buy_now = request.POST.get('buy_now') == 'true'
    
    if not sku_id:
        # If no SKU selected, try to get the first available SKU
        first_sku = product.skus.filter(stock__gt=0).first()
        if first_sku:
            sku = first_sku
        else:
            # No SKUs available at all
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'Out of stock'})
            return redirect('products:product_detail', pk=product_id)
    else:
        sku = get_object_or_404(SKU, pk=sku_id, product=product)
    
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, sku=sku)
    
    if not created:
        # Item already exists in cart
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True, 
                'message': 'Already added to cart',
                'cart_count': cart.total_items
            })
        # For non-AJAX requests (like Buy Now), we might still want to proceed to checkout
        # or show a message. For Buy Now, if it's already there, just redirect.
        if buy_now:
            return redirect('orders:checkout')
            
        return redirect('orders:view_cart')
    else:
        cart_item.quantity = quantity
        cart_item.save()
    
    if buy_now:
        return redirect('orders:checkout')
        
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True, 
            'message': 'Added to cart',
            'cart_count': cart.total_items
        })
    
    return redirect('orders:view_cart')

def view_cart(request):
    cart = _get_cart(request)
    return render(request, 'orders/cart.html', {'cart': cart})

@require_POST
def update_cart(request, item_id):
    cart = _get_cart(request)
    item = get_object_or_404(CartItem, pk=item_id, cart=cart)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > 0:
        # Check stock availability
        if quantity > item.sku.stock:
            quantity = item.sku.stock
            
        item.quantity = quantity
        item.save()
    else:
        item.delete()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_total_items': cart.total_items,
            'cart_total_price': cart.total_price,
            'item_quantity': item.quantity if quantity > 0 else 0,
            'item_total_price': item.total_price if quantity > 0 else 0,
            'item_id': item.id,
            'is_removed': quantity <= 0
        })

    return redirect('orders:view_cart')

def remove_from_cart(request, item_id):
    cart = _get_cart(request)
    item = get_object_or_404(CartItem, pk=item_id, cart=cart)
    item.delete()
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_total_items': cart.total_items,
            'cart_total_price': cart.total_price,
            'is_removed': True
        })
        
    return redirect('orders:view_cart')
