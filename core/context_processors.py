from orders.models import Cart
from wishlist.models import Wishlist

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

def _get_wishlist(request):
    if request.user.is_authenticated:
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    else:
        session_id = request.session.get('cart_session_id') # Reuse cart session
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
            request.session['cart_session_id'] = session_id
        wishlist, created = Wishlist.objects.get_or_create(session_id=session_id)
    return wishlist

def cart_wishlist_counts(request):
    """
    Context processor to provide global cart and wishlist counts.
    """
    if 'admin' in request.path:
        return {}
        
    cart = _get_cart(request)
    wishlist = _get_wishlist(request)
    
    return {
        'global_cart_count': cart.total_items,
        'global_wishlist_count': wishlist.items.count()
    }
