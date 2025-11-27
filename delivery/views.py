from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Shipment

@login_required
def dashboard(request):
    if request.user.role != 'DELIVERY':
        return redirect('core:home')
    
    # In a real app, shipments would be assigned to specific delivery partners.
    # For MVP, we'll show all shipments that are READY_TO_SHIP or SHIPPED.
    shipments = Shipment.objects.filter(status__in=[Shipment.Status.READY_TO_SHIP, Shipment.Status.SHIPPED])
    return render(request, 'delivery/dashboard.html', {'shipments': shipments})

@login_required
def shipment_detail(request, pk):
    if request.user.role != 'DELIVERY':
        return redirect('core:home')
        
    shipment = get_object_or_404(Shipment, pk=pk)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'mark_shipped':
            shipment.status = Shipment.Status.SHIPPED
            shipment.save()
        elif action == 'mark_delivered':
            shipment.status = Shipment.Status.DELIVERED
            shipment.save()
            
            # Check if all shipments for the order are delivered
            order = shipment.order
            if not order.shipments.exclude(status=Shipment.Status.DELIVERED).exists():
                # All shipments delivered, but order status might remain PAID or move to COMPLETED if we had that status.
                pass
                
        return redirect('delivery:dashboard')
        
    return render(request, 'delivery/shipment_detail.html', {'shipment': shipment})
