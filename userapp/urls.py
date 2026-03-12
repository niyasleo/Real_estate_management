from django.urls import path
from userapp import views
urlpatterns=[
    path('register/',views.register,name='register'),
    path('registration/',views.registration,name='registration'),
    path('login/',views.login,name='login'),
    path('login_view/',views.login_view,name='login_view'),
    path('otp/',views.otp,name='otp'),
    path('login_otp_verify/',views.login_otp_verify,name='login_otp_verify'),
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('properties/',views.properties,name='properties'),
    path('contact/',views.contact,name='contact'),
    path('single_page/<int:pid>',views.single_page,name='single_page'),
    path('enquiry_details/<int:pid>',views.enquiry_details,name='enquiry_details'),


    path('agent_home/',views.agent_home,name='agent_home'),
    path('enquiry/',views.enquiry,name='enquiry'),
    path('listed_properties/',views.listed_properties,name='listed_properties'),
    path('add_property/',views.add_property,name='add_property'),
    path('edit_property/<int:pid>',views.edit_property,name='edit_property'),
    path('update_property/<int:pid>',views.update_property,name='update_property'),
    path('delete_property/<int:pid>',views.delete_property,name='delete_property'),
    path('filter_property/',views.filter_property,name='filter_property'),
    path('filter_id/',views.filter_id,name='filter_id'),
    path('property_filter/',views.property_filter,name='property_filter'),
    path('logout_view/',views.logout_view,name='logout_view'),
]