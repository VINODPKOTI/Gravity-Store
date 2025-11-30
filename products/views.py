from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product, Category

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(is_active=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category__in=category.get_descendants(include_self=True))

    search_query = request.GET.get('q')
    if search_query:
        products = products.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))

    return render(request, 'products/product_list.html', {
        'category': category,
        'categories': categories,
        'products': products,
        'search_query': search_query
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    skus = product.skus.filter(stock__gt=0)
    return render(request, 'products/product_detail.html', {'product': product, 'skus': skus})

from django.http import JsonResponse

def product_search_suggestions(request):
    query = request.GET.get('q', '')
    if len(query) < 2:
        return JsonResponse({'results': []})

    products = Product.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query),
        is_active=True
    )[:5]

    results = []
    for product in products:
        results.append({
            'id': product.id,
            'title': product.title,
            'price': product.discounted_price if product.get_active_offer() else product.base_price,
            'url': f"/products/{product.id}/" # Assuming standard URL structure, ideally use reverse() but simpler for JSON here
        })
    
    return JsonResponse({'results': results})
