from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from products.models import Product
from products.forms import ProductForm
from .models import Seller

@login_required
def dashboard(request):
    # Ensure user is a seller
    if request.user.role != 'SELLER':
        return redirect('core:home')
    
    seller_profile, created = Seller.objects.get_or_create(user=request.user, defaults={'business_name': request.user.username})
    products = Product.objects.filter(seller=seller_profile)
    return render(request, 'sellers/dashboard.html', {'seller': seller_profile, 'products': products})

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
