from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Offer
from .forms import OfferForm

@login_required
def offer_list(request):
    if request.user.role != 'ADMIN':
        return redirect('core:home')
    offers = Offer.objects.all()
    return render(request, 'promotions/offer_list.html', {'offers': offers})

@login_required
def offer_add(request):
    if request.user.role != 'ADMIN':
        return redirect('core:home')
    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('promotions:offer_list')
    else:
        form = OfferForm()
    return render(request, 'promotions/offer_form.html', {'form': form, 'title': 'Add Offer'})

@login_required
def offer_edit(request, pk):
    if request.user.role != 'ADMIN':
        return redirect('core:home')
    offer = get_object_or_404(Offer, pk=pk)
    if request.method == 'POST':
        form = OfferForm(request.POST, instance=offer)
        if form.is_valid():
            form.save()
            return redirect('promotions:offer_list')
    else:
        form = OfferForm(instance=offer)
    return render(request, 'promotions/offer_form.html', {'form': form, 'title': 'Edit Offer'})
