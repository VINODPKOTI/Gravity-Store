from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import Shipment
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.db.models import Q, Sum

@login_required
def dashboard(request):
    if request.user.role != 'DELIVERY':
        return redirect('core:home')

    stats = {
        'ready': Shipment.objects.filter(status=Shipment.Status.READY_TO_SHIP).count(),
        'out': Shipment.objects.filter(status=Shipment.Status.OUT_FOR_DELIVERY).count(),
        'shipped': Shipment.objects.filter(status=Shipment.Status.SHIPPED).count(),
        'delivered': Shipment.objects.filter(status=Shipment.Status.DELIVERED).count(),
    }

    chart_data = (
        Shipment.objects
        .values('status')
        .annotate(total=Count('id'))
    )

    recent_shipments = Shipment.objects.order_by('-updated_at')[:5]

    return render(request, 'delivery/dashboard.html', {
        'stats': stats,
        'chart_data': chart_data,
        'recent_shipments': recent_shipments
    })


@login_required
def shipment_list(request):
    if request.user.role != 'DELIVERY':
        return redirect('core:home')

    # Handle status updates (same as before)
    if request.method == "POST":
        shipment_id = request.POST.get("shipment_id")
        action = request.POST.get("action")

        shipment = Shipment.objects.filter(id=shipment_id).first()
        if shipment:
            if action == "mark_shipped":
                shipment.status = Shipment.Status.SHIPPED
            elif action == "mark_out":
                shipment.status = Shipment.Status.OUT_FOR_DELIVERY
            elif action == "mark_delivered":
                shipment.status = Shipment.Status.DELIVERED
            shipment.save()
        return redirect("delivery:shipment_list")

    # 🔍 SEARCH
    search = request.GET.get("q", "")

    shipments_qs = Shipment.objects.filter(
        status__in=[
            Shipment.Status.READY_TO_SHIP,
            Shipment.Status.SHIPPED,
            Shipment.Status.OUT_FOR_DELIVERY
        ]
    ).select_related("order", "seller")

    if search:
        shipments_qs = shipments_qs.filter(
            Q(id__icontains=search) |
            Q(order__id__icontains=search) |
            Q(seller__business_name__icontains=search)
        )

    # 📦 TOTAL QUANTITY PER SHIPMENT
    shipments_qs = shipments_qs.annotate(
        total_qty=Sum("order__items__quantity")
    ).order_by("-updated_at")

    paginator = Paginator(shipments_qs, 10)
    page_number = request.GET.get("page")
    shipments = paginator.get_page(page_number)

    return render(request, "delivery/shipment_list.html", {
        "shipments": shipments,
        "search": search
    })

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




@login_required
def shipment_history(request):
    if request.user.role != "DELIVERY":
        return redirect("core:home")

    shipments_qs = Shipment.objects.filter(
        status__in=[
            Shipment.Status.DELIVERED,
            Shipment.Status.CANCELLED
        ]
    ).select_related("order", "seller").order_by("-updated_at")

    paginator = Paginator(shipments_qs, 15)
    page_number = request.GET.get("page")
    shipments = paginator.get_page(page_number)

    return render(request, "delivery/shipment_history.html", {
        "shipments": shipments
    })