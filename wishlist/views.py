from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import Wishlist, WishlistItem
from products.models import Product, SKU


def _get_wishlist(request):
    """Helper function to get or create wishlist for user or guest session"""
    if request.user.is_authenticated:
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    else:
        session_id = request.session.get('cart_session_id')  # Reuse cart session
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
            request.session['cart_session_id'] = session_id
        wishlist, created = Wishlist.objects.get_or_create(session_id=session_id)
    return wishlist


def wishlist_view(request):
    """Display the user's wishlist"""
    wishlist = _get_wishlist(request)
    return render(request, 'wishlist/wishlist.html', {'wishlist': wishlist})


@require_POST
def add_to_wishlist(request, product_id):
    """Toggle a product in wishlist (Add/Remove)"""
    product = get_object_or_404(Product, pk=product_id)
    wishlist = _get_wishlist(request)
    
    sku_id = request.POST.get('sku')
    sku = None
    if sku_id:
        sku = get_object_or_404(SKU, pk=sku_id, product=product)
    
    # Check if already in wishlist
    existing_item = WishlistItem.objects.filter(
        wishlist=wishlist,
        product=product,
        sku=sku
    ).first()
    
    if not existing_item:
        # Add to wishlist
        WishlistItem.objects.create(
            wishlist=wishlist,
            product=product,
            sku=sku
        )
        message = 'Added to wishlist'
        action = 'added'
    else:
        # Remove from wishlist
        existing_item.delete()
        message = 'Removed from wishlist'
        action = 'removed'
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': message,
            'action': action,
            'wishlist_count': wishlist.items.count()
        })
    
    from django.shortcuts import redirect
    return redirect('wishlist:wishlist')


def remove_from_wishlist(request, item_id):
    """Remove an item from wishlist"""
    wishlist = _get_wishlist(request)
    item = get_object_or_404(WishlistItem, pk=item_id, wishlist=wishlist)
    item.delete()
    
    from django.shortcuts import redirect
    return redirect('wishlist:wishlist')


@require_POST
def move_to_cart(request, item_id):
    """Move an item from wishlist to cart"""
    from orders.models import Cart, CartItem
    from orders.views import _get_cart
    
    # Get wishlist item
    wishlist = _get_wishlist(request)
    wishlist_item = get_object_or_404(WishlistItem, pk=item_id, wishlist=wishlist)
    
    # Get or create cart
    cart = _get_cart(request)
    
    # Determine SKU to use
    sku = wishlist_item.sku
    if not sku:
        # If wishlist item doesn't have a SKU, get the first available one
        sku = wishlist_item.product.skus.filter(stock__gt=0).first()
        if not sku:
            # No SKUs available at all
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Product is out of stock'
                })
            from django.shortcuts import redirect
            return redirect('wishlist:wishlist')
    
    # Add to cart
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=wishlist_item.product,
        sku=sku
    )
    
    if not created:
        # Item already exists in cart, just update quantity
        cart_item.quantity += 1
        cart_item.save()
        message = 'Item already in cart, quantity increased'
    else:
        # New item added to cart
        cart_item.quantity = 1
        cart_item.save()
        message = 'Moved to cart'
    
    # Remove from wishlist
    wishlist_item.delete()
    
    # Return JSON for AJAX or redirect for regular requests
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': message,
            'cart_count': cart.total_items,
            'wishlist_count': wishlist.items.count()
        })
    
    from django.shortcuts import redirect
    return redirect('wishlist:wishlist')
