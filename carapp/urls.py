from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('aboutus', views.aboutus, name='aboutus'),
    path('carapp/<int:cartype_no>', views.cardetail, name='cardetail'),
    # path('lab-group/', views.lab_group_members, name='lab_group_members'),
    path('lab-group/', views.LabGroupMembersView.as_view(), name='lab_group_members'),
]