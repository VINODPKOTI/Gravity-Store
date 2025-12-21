from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product, Category
import json
from django.http import JsonResponse
from .models import SKU
import traceback

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

    # Get wishlist items for checking
    wishlist_product_ids = []
    if request.user.is_authenticated:
        from wishlist.models import Wishlist
        wishlist = Wishlist.objects.filter(user=request.user).first()
        if wishlist:
            wishlist_product_ids = list(wishlist.items.values_list('product_id', flat=True))
    else:
        session_id = request.session.get('cart_session_id')
        if session_id:
            from wishlist.models import Wishlist
            wishlist = Wishlist.objects.filter(session_id=session_id).first()
            if wishlist:
                wishlist_product_ids = list(wishlist.items.values_list('product_id', flat=True))

    return render(request, 'products/product_list.html', {
        'category': category,
        'categories': categories,
        'products': products,
        'search_query': search_query,
        'wishlist_product_ids': wishlist_product_ids
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    skus = product.skus.filter(stock__gt=0)

    # 🔹 Convert SKU attributes to JSON for the template
    for sku in skus:
        sku.attrs_json = json.dumps(sku.attributes or {})

    # Check if in wishlist
    in_wishlist = False
    if request.user.is_authenticated:
        from wishlist.models import Wishlist
        wishlist = Wishlist.objects.filter(user=request.user).first()
        if wishlist:
            in_wishlist = wishlist.items.filter(product=product).exists()
    else:
        session_id = request.session.get('cart_session_id')
        if session_id:
            from wishlist.models import Wishlist
            wishlist = Wishlist.objects.filter(session_id=session_id).first()
            if wishlist:
                in_wishlist = wishlist.items.filter(product=product).exists()

    return render(request, 'products/product_detail.html', {
        'product': product,
        'skus': skus,
        'in_wishlist': in_wishlist
    })



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



def get_sku_attributes(request, sku_id):
    """
    Returns SKU attributes as JSON for AJAX requests
    """
    try:
        sku = SKU.objects.get(pk=sku_id)
        return JsonResponse({
            'attributes': sku.attributes or {}
        })
    except SKU.DoesNotExist:
        return JsonResponse({'attributes': {}}, status=404)
    except Exception as e:
        print("Error in get_sku_attributes:", e)
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)