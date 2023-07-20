import json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import OrderVehicle, Vehicle, CarType, LabGroupMember, Buyer, User
from django.views.generic.list import ListView
from .forms import OrderVehicleForm
from datetime import date
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse


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
    session_visit_count = request.session.get('aboutus_visits', 0)
    request.session['aboutus_visits'] = session_visit_count + 1
    message = "This is a Car Showroom. Session count for this page = " + str(session_visit_count)
    # request.session.flush()
    response = render(request, 'carapp/aboutus.html', {'message': message})

    # Cookies
    print(request.COOKIES)
    if 'cookie_counter' in request.COOKIES:
        print("Cookie is set.")
    else:
        print("Setting a cookie")
        # setting a cookie named 'cookie_counter' with value '10' that expires in 10 seconds
        response.set_cookie('cookie_counter', '10', max_age=10)
    return response


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
    Compared to the Function Based View (FBV) the CBV inherits the properties of ListView and the method
    get_context_data() is used to get all the details.
    By using the ListView class, the CBV handles fetching the queryset of LabGroupMember objects from the database automatically.
    It also provides pagination functionality if needed. The context data, including the list of lab group members,
    is made available in the template using the specified context_object_name.
    """
    model = LabGroupMember
    template_name = "labgroupmembers_list.html"

    def get_context_data(self, **kwargs):
        members = super().get_context_data(**kwargs)
        return members

def vehicles(request):
    """ functions to display vehicles """
    vehicles_list = Vehicle.objects.all()
    if len(vehicles_list) != 0 or vehicles_list is not None:
        return render(request, "carapp/vehicles.html", {"vehicles_list": vehicles_list})
    return render(request, "carapp/vehicles.html")

def orderhere(request):
    msg = ''
    vehiclelist = Vehicle.objects.all()
    if request.method == 'POST':
        form = OrderVehicleForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            vehicle = Vehicle.objects.get(car_name = order.vehicle)
            if order.number_of_Vehicles <= vehicle.inventory:
                buyer_id = User.objects.get(first_name = order.buyer).id
                orders = OrderVehicle(number_of_Vehicles = order.number_of_Vehicles,
                                      status = 1,
                                      order_date = date.today(),
                                      buyer_id = buyer_id,
                                      vehicle_id = vehicle.id)
                orders.save()

                vehicle.inventory -= order.number_of_Vehicles
                if vehicle.inventory == 0:
                    vehicle.instock = 0
                vehicle.save()
                msg = 'Your vehicle has been ordered'
                return HttpResponse(msg)
            else:
                msg = 'We do not have sufficient stock to fill your order.'
                return render(request, 'carapp/nosuccess_order.html', {'msg': msg})
    else:
        form = OrderVehicleForm()
        return render(request, 'carapp/orderhere.html', {'form': form, 'msg': msg, 'vehicles_list': vehiclelist})

def filter_price(request):
    if request.method == 'POST':
        vehicle_name = request.POST.get('vehicle')
        vehicle = get_object_or_404(Vehicle, car_name=vehicle_name)
        response = vehicle.car_price
        return render(request, 'carapp/carprice.html', {'price': response ,'vehicles': Vehicle.objects.all(),'selected_vehicle': vehicle})
    else:
        return render(request, 'carapp/carprice.html', {'vehicles': Vehicle.objects.all()})

def login_here(request):
    """ path = 'login """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('carapp:homepage'))
            else:
                return HttpResponse('Your account is disabled')
        else:
            return HttpResponse('Login details are incorrect')
    else:
        return render(request, 'carapp/login_here.html')

@login_required
def logout_here(request):
    """ path='logout' """
    logout(request)
    return HttpResponseRedirect(reverse('carapp:homepage'))

@login_required
def list_of_orders(request):
    """ path = 'orders' """
    user = request.user
    template = "carapp/list_of_orders.html"
    # Check if the user is a buyer
    users = User.objects.filter(id=user.id)
    # condition when user is not valid
    if users is not None and len(users) != 0:
        user = users[0]
        buyers = Buyer.objects.filter(pk=user.id)
        # condition when there are no buyers with this user details
        if len(buyers) == 0:
            message = 'You are not registered'
            return render(request, template, {'message': message})
        buyer = buyers[0]
        orders = OrderVehicle.objects.filter(buyer=buyer)
        if len(orders) == 0:
            message = "No orders placed yet."
            return render(request, template, {'message': message})
        return render(request, template, {'orders': orders})
    else:
        message = 'You are not registered'
        return render(request, template, {'message': message})


