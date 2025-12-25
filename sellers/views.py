from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from products.models import Product
from products.forms import ProductForm
from .models import Seller
from django.db.models import Prefetch, Sum, F
from orders.models import Order, OrderItem
from django.db.models.functions import TruncHour, TruncDay, TruncWeek, TruncMonth
from django.utils.timezone import now
from datetime import timedelta,datetime
import calendar

@login_required
def dashboard(request):
    if request.user.role != 'SELLER':
        return redirect('core:home')

    seller, _ = Seller.objects.get_or_create(
        user=request.user,
        defaults={'business_name': request.user.username}
    )

    products = Product.objects.filter(seller=seller)
    order_items = OrderItem.objects.filter(product__seller=seller)

    # Stats
    total_orders = Order.objects.filter(items__product__seller=seller).distinct().count()
    pending_orders = Order.objects.filter(items__product__seller=seller, status='PENDING').distinct().count()
    total_earnings = order_items.aggregate(total=Sum(F('price') * F('quantity')))['total'] or 0
    recent_orders = Order.objects.filter(items__product__seller=seller).distinct().order_by('-created_at')[:5]

    # ===== Sales Data =====

    today = datetime.today()

    # 1️⃣ Hourly sales today
    hourly_qs = order_items.filter(order__created_at__date=today.date()) \
        .annotate(hour=TruncHour('order__created_at')) \
        .values('hour') \
        .annotate(total=Sum(F('price') * F('quantity'))) \
        .order_by('hour')
    today_labels = [entry['hour'].strftime("%H:%M") for entry in hourly_qs]
    today_totals = [float(entry['total']) for entry in hourly_qs]

    # 2️⃣ Weekly sales (last 4 weeks)
    four_weeks_ago = today - timedelta(weeks=4)
    weekly_qs = order_items.filter(order__created_at__gte=four_weeks_ago) \
        .annotate(week=TruncWeek('order__created_at')) \
        .values('week') \
        .annotate(total=Sum(F('price') * F('quantity'))) \
        .order_by('week')
    weekly_labels = [entry['week'].strftime("%d %b") for entry in weekly_qs]
    weekly_totals = [float(entry['total']) for entry in weekly_qs]

    # 3️⃣ Monthly sales (last 12 months)
    monthly_qs = order_items.annotate(month=TruncMonth('order__created_at')) \
        .values('month') \
        .annotate(total=Sum(F('price') * F('quantity'))) \
        .order_by('month')
    monthly_labels = [entry['month'].strftime("%b %Y") for entry in monthly_qs]
    monthly_totals = [float(entry['total']) for entry in monthly_qs]

    context = {
        'seller': seller,
        'products': products,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'total_earnings': total_earnings,
        'recent_orders': recent_orders,
        'today_labels': today_labels,
        'today_totals': today_totals,
        'weekly_labels': weekly_labels,
        'weekly_totals': weekly_totals,
        'monthly_labels': monthly_labels,
        'monthly_totals': monthly_totals,
    }

    return render(request, 'sellers/dashboard.html', context)

@login_required
def product_list(request):
    if request.user.role != 'SELLER':
        return redirect('core:home')
    seller = request.user.seller_profile
    products = Product.objects.filter(seller=seller)
    return render(request, 'sellers/product_list.html', {'products': products})

@login_required
def product_add(request):
    if request.user.role != 'SELLER':
        return redirect('core:home')
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user.seller_profile
            product.save()
            return redirect('sellers:product_list')
    else:
        form = ProductForm()
    return render(request, 'sellers/product_form.html', {'form': form, 'title': 'Add Product'})

@login_required
def product_edit(request, pk):
    if request.user.role != 'SELLER':
        return redirect('core:home')
        
    product = get_object_or_404(Product, pk=pk, seller=request.user.seller_profile)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('sellers:product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'sellers/product_form.html', {'form': form, 'title': 'Edit Product'})

@login_required
def product_delete(request, pk):
    if request.user.role != 'SELLER':
        return redirect('core:home')
    product = get_object_or_404(
        Product,
        pk=pk,
        seller=request.user.seller_profile
    )
    if request.method == 'POST':
        product.delete()
        return redirect('sellers:product_list')
    return redirect('sellers:product_list')

@login_required
def seller_orders(request):
    if request.user.role != 'SELLER':
        return redirect('core:home')

    seller = request.user.seller_profile

    orders = (
        Order.objects
        .filter(items__product__seller=seller)
        .distinct()
        .prefetch_related(
            Prefetch(
                'items',
                queryset=OrderItem.objects.select_related('product').filter(
                    product__seller=seller
                ),
                to_attr='seller_items'
            )
        )
        .order_by('-created_at')
    )

    # ✅ ADD THIS BLOCK
    for order in orders:
        order.seller_total = sum(
            item.price * item.quantity
            for item in order.seller_items
        )

    return render(
        request,
        'sellers/seller_orders.html',
        {'orders': orders}
    )


@login_required
def seller_order_detail(request, order_id):
    if request.user.role != 'SELLER':
        return redirect('core:home')

    seller = request.user.seller_profile
    order = get_object_or_404(Order, id=order_id)

    items = OrderItem.objects.filter(
        order=order,
        product__seller=seller
    )

    # ✅ attach row_total to each item
    for item in items:
        item.row_total = item.price * item.quantity

    seller_total = sum(item.row_total for item in items)

    context = {
        'order': order,
        'items': items,
        'seller_total': seller_total,
        'buyer': order.user,
        'address': order.shipping_address,
    }
    return render(request, 'sellers/order_detail.html', context)

