from django.shortcuts import render,redirect
from adminapp.models import *
from userapp.models import *
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User


def dashboard(request):
    user=Users.objects.filter(role__in=['Agent','Owner']).count()
    list=Property.objects.all().count()

    today = timezone.now().date()
    latest = Enquiry.objects.filter(
        created_at__date=today
    ).count()

    return render(request,'dashboard.html',{'user':user,'list':list,'latest':latest})

def property_type(request):
    return render(request,'property_type.html')

def display_property_type(request):
    data=Property_type.objects.all()
    return render(request,'display_property_type.html',{'data':data})

def add_property_type(request):
    if request.method == "POST":
        property_name = request.POST.get('property')
        Property_type.objects.create(property_types=property_name)
    return redirect(property_type)

def delete_property_type(request,pid):
    obj = Property_type.objects.get(id=pid)
    obj.delete()
    return redirect(display_property_type)

def admin_register(request):
    return render(request,'admin.html')


def admin_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')


        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['username']=username
            messages.success(request,'Welcome Admin ')
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials")

    return render(request, 'admin.html')


# 2. This view handles ONLY the Registration
def admin_register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        else:
            user = User.objects.create_user(username=username,  password=password)
            user.save()
            messages.success(request, "Registration successful! Please login.")

    return redirect(admin_register)






def admin_logout(request):
    del request.session['username']
    messages.success(request,'sccessfully logged out')
    return redirect(admin_register)
def message(request):
    submissions = ContactMessage.objects.all().order_by('-id')
    return render(request,'messages.html',{'contact_data': submissions})


def contact_view(request):
    if request.method == "POST":
        full_name = request.POST.get('name')
        email = request.POST.get('email')
        role = request.POST.get('role')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        ContactMessage.objects.create(
            full_name=full_name,
            email=email,
            role=role,
            subject=subject,
            message=message
        )
        messages.success(request,'Message sent succesfully')
        return redirect('contact')  # reload page after submit

    return render(request, 'contact.html')
def all_property(request):
    # Fetch all properties, newest first
    properties = Property.objects.all().order_by('-id')

    # Pass them to the template
    return render(request, 'all_properties.html', {'data': properties})
def agent_list(request):
    data=Users.objects.filter(role__in=['Agent','Owner'])
    return render(request,'agent_list.html',{'data':data})
def delete_msg(request,mid):
    data=ContactMessage.objects.get(id=mid)
    data.delete()
    return redirect(message)