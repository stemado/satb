from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string


import markdown
from careplus.physicianorders.forms import PhysicianOrderForm
from careplus.physicianorders.models import PhysicianOrder
from careplus.decorators import ajax_required

def _orders(request, orders):
	return render(request, 'physicianorders/orders.html', {
		'orders': orders
		})


@login_required
def orders(request):
	all_orders = PhysicianOrder.get_orders()
	return _orders(request, all_orders)

#Check here to see if this view is correct.
@login_required
def order(request, id):
    order = get_object_or_404(PhysicianOrder, id=id)
    return render(request, 'physicianorders/order.html', {'order': order})


@login_required
def createPhysicianOrder(request):
    if request.method == 'POST':
        form = PhysicianOrderForm(request.POST)
        if form.is_valid():
            physicianOrder = PhysicianOrder()
            physicianOrder.orderMedication = form.cleaned_data.get('orderMedication')
            physicianOrder.orderDetails = form.cleaned_data.get('orderDetails')
            physicianOrder.orderTime = form.cleaned_data.get('orderTime')
            physicianOrder.orderPhysician = form.cleaned_data.get('orderPhysician')
            physicianOrder.orderDate = form.cleaned_data.get('orderDate')
            physicianOrder.save()
            return redirect('orders')
    else:
        form = PhysicianOrderForm()
    return render(request, 'physicianorders/create_physician_order.html', {'form': form})


def editPhysicianOrder(request, id):
    if id:
        order = get_object_or_404(PhysicianOrder, pk=id)
    else:
        order = None

    if request.method == 'POST':
        form = PhysicianOrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/physicianorders/')
    else: 
        form = PhysicianOrderForm(instance=order, initial={'orders': orders})
    return render(request, 'physicianorders/edit_physician_order.html', {'form': form})



