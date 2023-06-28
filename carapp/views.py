import json
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import OrderVehicle, Vehicle, CarType, LabGroupMember
from django.views.generic.list import ListView


def homepage(request):
    # """ function that displays vehicles in the descending order of car price. path='' """
    # vehicle_list = Vehicle.objects.all().order_by('car_price')
    # response = HttpResponse()
    # heading1 = '<p>' + 'Vehicles Sorted by car price (Expensive first): ' + '</p>'
    # response.write(heading1)
    # count = 0
    # for index in range(len(vehicle_list)-1, -1, -1):
    #     count = count+1
    #     if count > 10:
    #         break
    #     para = '<p>' + str(vehicle_list[index].car_name) + '&nbsp &nbsp &nbsp &nbsp ' + str(vehicle_list[index].car_price) + '</p>'
    #     response.write(para)

    # return response
    cartype_list = CarType.objects.all().order_by('id')
    return render(request, 'carapp/homepage.html', {'cartype_list': cartype_list})


def aboutus(request):
    """ path='aboutus' """
    # return HttpResponse("This is a Car Showroom.")
    return render(request, 'carapp/aboutus.html', {'message': "This is a Car Showroom"})


def cardetail(request, cartype_no):
    """ function to display a list of vehicles of requested car type. path='carapp/<int:cartype_no>'"""
    car_type = get_object_or_404(CarType, id=cartype_no)
    vehicles = Vehicle.objects.filter(car_type=car_type)
    response = HttpResponse()
    # para = '<p>' + "Car type: " + str(car_type.name) + '<p> Vehicles: <br>'
    # response.write(para)
    # for vehicle in vehicles:
    #     para = '<p>' + str(vehicle.car_name) + '</p>'
    #     response.write(para)
    return render(request, 'carapp/cardetail.html', {'vehicles_list': vehicles})


def lab_group_members(request):
    """ function to display lab group members details ordered by first name, path='lab-group/' """
    members = LabGroupMember.objects.all()
    response = HttpResponse()
    para = '<h3> Lab Group Members Details </h3>'
    response.write(para)
    for member in members:
        para = '<p>' + str(member.first_name) + ', ' + str(member.last_name) + ', ' + str(member.semester) + ', ' + str(
            member.url) + '<p>'
        response.write(para)
    return response


class LabGroupMembersView(ListView):
    """
    Class Based View (CBV) to display lab group members details ordered by first name, path='lab-group/'
    Compared to the Function Based View (FBV) the CBV inherits the properties of ListView and the method get_context_data() is used to get all the details.
    By using the ListView class, the CBV handles fetching the queryset of LabGroupMember objects from the database automatically.
    It also provides pagination functionality if needed. The context data, including the list of lab group members,
    is made available in the template using the specified context_object_name.
    """
    model = LabGroupMember
    template_name = "labgroupmembers_list.html"

    def get_context_data(self, **kwargs):
        members = super().get_context_data(**kwargs)
        return members
