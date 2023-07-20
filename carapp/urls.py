from django.urls import path
from . import views
app_name = 'carapp'
urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('aboutus', views.aboutus, name='aboutus'),
    path('carapp/<int:cartype_no>', views.cardetail, name='cardetail'),
    # path('lab-group/', views.lab_group_members, name='lab_group_members'),
    path('lab-group/', views.LabGroupMembersView.as_view(), name='lab_group_members'),
    path('vehicles', views.vehicles, name='vehicles'),
    path('orderhere/', views.orderhere, name='orderhere'),
    path('login/', views.login_here, name='login'),
    path('logout/', views.logout_here, name='logout'),
    path('orders/', views.list_of_orders, name='orders_list'),
]