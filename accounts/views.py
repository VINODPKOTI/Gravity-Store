from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, AddressForm
from .models import Address

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = user.Role.CUSTOMER  # Default all new users to Customer
            user.save()
            login(request, user)
            return redirect('core:home')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def address_list(request):
    addresses = Address.objects.filter(user=request.user)
    return render(request, 'accounts/address_list.html', {'addresses': addresses})

@login_required
def address_add(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Address added successfully',
                    'address': {
                        'id': address.id,
                        'full_name': address.full_name,
                        'street_address': address.street_address,
                        'city': address.city,
                        'state': address.state,
                        'postal_code': address.postal_code,
                        'phone_number': address.phone_number
                    }
                })

            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('accounts:address_list')
    else:
        form = AddressForm()
    return render(request, 'accounts/address_form.html', {'form': form, 'title': 'Add Address'})

@login_required
def address_edit(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('accounts:address_list')
    else:
        form = AddressForm(instance=address)
    return render(request, 'accounts/address_form.html', {'form': form, 'title': 'Edit Address'})

@login_required
def address_delete(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    if request.method == 'POST':
        address.delete()
        return redirect('accounts:address_list')
    return render(request, 'accounts/address_confirm_delete.html', {'address': address})

@login_required
def profile(request):
    from .forms import UserProfileForm
    from django.contrib import messages
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'accounts/profile.html', {'form': form})

def custom_login(request):
    from django.contrib.auth import authenticate, login as auth_login
    from django.contrib import messages
    from orders.models import Cart, CartItem
    from wishlist.models import Wishlist, WishlistItem
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Get guest cart/wishlist before login
            guest_cart_id = None
            guest_wishlist_id = None
            
            if not request.user.is_authenticated:
                session_id = request.session.get('cart_session_id')
                if session_id:
                    try:
                        guest_cart = Cart.objects.get(session_id=session_id)
                        guest_cart_id = guest_cart.id
                    except Cart.DoesNotExist:
                        pass
                    
                    try:
                        guest_wishlist = Wishlist.objects.get(session_id=session_id)
                        guest_wishlist_id = guest_wishlist.id
                    except Wishlist.DoesNotExist:
                        pass
            
            # Login the user
            auth_login(request, user)
            # Merge guest cart into user cart
            if guest_cart_id:
                try:
                    guest_cart = Cart.objects.get(id=guest_cart_id)
                    user_cart, created = Cart.objects.get_or_create(user=user)
                    
                    for item in guest_cart.items.all():
                        # Check if item already exists in user cart
                        existing_item = CartItem.objects.filter(
                            cart=user_cart,
                            product=item.product,
                            sku=item.sku
                        ).first()
                        
                        if existing_item:
                            # Update quantity
                            existing_item.quantity += item.quantity
                            existing_item.save()
                        else:
                            # Move item to user cart
                            item.cart = user_cart
                            item.save()
                    
                    # Delete guest cart
                    guest_cart.delete()
                except Cart.DoesNotExist:
                    pass
            
            # Merge guest wishlist into user wishlist
            if guest_wishlist_id:
                try:
                    guest_wishlist = Wishlist.objects.get(id=guest_wishlist_id)
                    user_wishlist, created = Wishlist.objects.get_or_create(user=user)
                    
                    for item in guest_wishlist.items.all():
                        # Check if item already exists in user wishlist
                        existing_item = WishlistItem.objects.filter(
                            wishlist=user_wishlist,
                            product=item.product,
                            sku=item.sku
                        ).first()
                        
                        if not existing_item:
                            # Move item to user wishlist
                            item.wishlist = user_wishlist
                            item.save()
                        else:
                            # Item already in wishlist, delete duplicate
                            item.delete()
                    # Delete guest wishlist
                    guest_wishlist.delete()
                except Wishlist.DoesNotExist:
                    pass
            
            messages.success(request, f'Welcome back, {user.username}!')
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/login.html')

