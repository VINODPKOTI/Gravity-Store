from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from accounts.models import User
from orders.models import Order
from products.models import Product

def home(request):
    return render(request, 'core/home.html')

@login_required
def admin_dashboard(request):
    if request.user.role != 'ADMIN':
        return redirect('core:home')
    
    total_sales = Order.objects.filter(status=Order.Status.PAID).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    total_orders = Order.objects.count()
    total_users = User.objects.count()
    total_products = Product.objects.count()
    
    recent_orders = Order.objects.order_by('-created_at')[:10]
    
    context = {
        'total_sales': total_sales,
        'total_orders': total_orders,
        'total_users': total_users,
        'total_products': total_products,
        'recent_orders': recent_orders,
    }
    return render(request, 'core/admin_dashboard.html', context)
