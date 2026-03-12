from django.urls import path
from adminapp import views

urlpatterns=[
    path('dashboard/',views.dashboard,name='dashboard'),
    path('property_type/',views.property_type,name='property_name'),
    path('display/',views.display_property_type,name='display_property'),

    path('add/',views.add_property_type,name='add_property_type'),
    path('delete_property/<int:pid>/',views.delete_property_type,name='delete_property_type'),

    path('admin_register/', views.admin_register, name='admin_register'),
    path('admin_register_view/', views.admin_register_view, name='admin_register_view'),
    path('admin_login_view/', views.admin_login_view, name='admin_login_view'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),
    path('message/', views.message, name='message'),
    path('save_contact/', views.contact_view, name='save_contact'),
    path('all_property/', views.all_property, name='all_property'),
    path('agent_list/', views.agent_list, name='agent_list'),
    path('delete_msg/<int:mid>', views.delete_msg, name='delete_msg'),

]