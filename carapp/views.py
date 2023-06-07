import json
from django.http import HttpResponse
from django.shortcuts import render
from .models import OrderVehicle, Vehicle


def test(request):
    query_param = request.GET.get('orderId')
    queryset1 = OrderVehicle.objects.filter(pk=query_param)
    price = OrderVehicle.total_price(queryset1[0])
    # return render(request, 'app/base.html', context)
    # json_data = json.dumps(queryset)
    # return HttpResponse(json_data)
    return  HttpResponse(price)