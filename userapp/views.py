from django.contrib.auth.hashers import make_password,check_password
from django.shortcuts import render,redirect
from userapp.models import *
from adminapp.models import *
from django.contrib import messages
import random
from twilio.rest import Client
from django.db.models import Q
from django.contrib.auth import logout
from django.conf import settings

def register(request):
    return render(request,'register.html')
def login(request):
    return render(request,'login.html')
def registration(request):
    if request.method=='POST':
        uname=request.POST.get('user')
        mobile=request.POST.get('mobile')
        upass=request.POST.get('password')
        confirm=request.POST.get('cpassword')
        encrypt=make_password(upass)
        Role=request.POST.get('role')

        if Users.objects.filter(name=uname).exists():
            messages.error(request,'username already exist.Please try another')
            return redirect(register)

        if upass!=confirm:
            messages.error(request,'password do not match try again')
            return redirect(register)
        if Users.objects.filter(mobile=mobile).exists():
            messages.error(request,'Phone number is already in use.Please try another')
            return redirect(register)


        Users.objects.create(name=uname,mobile=mobile,password=encrypt,role=Role)
    return redirect(login)


def send_otp(mobile):
    client = Client(settings.TWILIO_ACCOUNT_SID,settings.TWILIO_AUTH_TOKEN)
        # FIX: The range must be (start, end) where start <= end.
        # For a 6-digit OTP, use 100000 to 999999.
    otp = str(random.randint(100000, 999999))

    message = client.messages.create(
            body=f'Your verification code is {otp}. It will expire in 5 minutes.',
            from_=settings.TWILIO_PHONE_NUMBER,
            to=f'+91{mobile}'
        )
    return otp



def login_view(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        upass = request.POST.get('pswd')

        # 1. Check if user exists
        user = Users.objects.filter(mobile=mobile).first()

        if not user:
            messages.error(request, 'Mobile number not registered. Please sign up.')
            return render(request, 'register.html') # Correct: New users go to register

        # 2. Check Password
        if check_password(upass, user.password):
            # 3. Correct pass, now try to send OTP
            otp_code = send_otp(mobile)

            if otp_code:
                # 4. Save/Update OTP in DB
                User_otp.objects.update_or_create(
                    mobile=mobile,
                    defaults={'otp': otp_code}
                )
                # Success: Go to OTP verification page
                return render(request, 'otp.html')
            else:
                messages.error(request, 'SMS service failed. Are you using a verified Twilio number?')
                return render(request, 'login.html') # Stay on login if SMS fails
        else:
            messages.error(request, 'Invalid Password. Please try again.')
            return render(request, 'login.html')

    # If GET request, show the login page
    return render(request, 'login.html')


def login_otp_verify(request):
    if request.method == 'POST':
        otp_entered = request.POST.get('otp')
        mobile = request.POST.get('mobile')


        user = Users.objects.filter(mobile=mobile).first()
        otp_record = User_otp.objects.filter(mobile=mobile, otp=otp_entered).last()



        if otp_record and user:
            # Check for expiration using your model method
            if otp_record.is_expired():
                messages.error(request, 'OTP has expired. Please request a new one.')
            else:
                # Success!
                otp_record.delete()

                request.session['user_id'] = user.id
                request.session['user_role'] = user.role
                request.session['username'] = user.name

                # Role-based redirect
                if user.role.lower() in ['agent', 'owner']:
                    return redirect('agent_home')
                return redirect('home')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')

        return render(request, 'otp.html')

    return redirect('login')

def otp(request):
    return render(request,'otp.html')

def home(request):
    data=Property_type.objects.all()
    properties = Property.objects.all().order_by('-id')[:6]
    return render(request,'home.html',{'data':data,'properties':properties})
def about(request):
    return render(request,'about.html')
def properties(request):
    data=Property.objects.all()
    type=Property_type.objects.all()

    return render(request,'properties.html',{'data':data,'type':type})
def contact(request):
     return render(request,'contact.html')

def single_page(request, pid):
    data = Property.objects.get(id=pid)
    return render(request, 'single_page.html',{'data':data})



def agent_home(request):
    data=Property_type.objects.all()
    count=Property.objects.count()
    today = timezone.now().date()
    latest = Enquiry.objects.filter(
        created_at__date=today
    ).count()
    return render(request,'agent_home.html',{'data':data,'count':count,'latest':latest})

def enquiry(request):
    data=Enquiry.objects.all().order_by('-id')
    return render(request,'enquiry.html',{'data':data})

def listed_properties(request):
    data = Property.objects.all()

    for p in data:
        p.enquiry_count = Enquiry.objects.filter(property_id=p.property_id).count()
    return render(request, 'listed_properties.html', {'data': data})

def add_property(request):
    if request.method == 'POST':

        title = request.POST.get('property_title')
        loc = request.POST.get('location')
        price = request.POST.get('price')
        area = request.POST.get('area')
        status = request.POST.get('status')
        beds = request.POST.get('bedrooms')
        baths = request.POST.get('bathrooms')
        type = request.POST.get('type')
        description = request.POST.get('description')

        img1 = request.FILES.get('property_image1')
        img2 = request.FILES.get('property_image2')
        img3 = request.FILES.get('property_image3')

        feature_list = request.POST.getlist('features')

        while True:
            generated_id = str(random.randint(100000, 999999))
            if not Property.objects.filter(property_id=generated_id).exists():
                break

        Property.objects.create(
            property_id=generated_id,
            property_title=title,
            location=loc,
            price=price,
            area=area,
            status=status,
            bedrooms=beds,
            bathrooms=baths,
            description=description,
            image1=img1,
            image2=img2,
            image3=img3,
            property_type=type,
            posted_by=request.session['user_role'],
            features=feature_list  # ✅ store list directly (JSONField)
        )

        messages.success(request, "Property added successfully!")
    return redirect(agent_home)

def update_property(request, pid):

    if request.method == 'POST':
        data=Property.objects.get(id=pid)
        data.property_title = request.POST.get('property_title')
        data.location = request.POST.get('location')
        data.price = request.POST.get('price')
        data.area = request.POST.get('area')
        data.status = request.POST.get('status')
        data.bedrooms = request.POST.get('bedrooms')
        data.bathrooms = request.POST.get('bathrooms')
        data.property_type = request.POST.get('type')
        data.description = request.POST.get('description')



        if request.FILES.get('property_image1'):
            data.image1 = request.FILES.get('property_image1')

        if request.FILES.get('property_image2'):
            data.image2 = request.FILES.get('property_image2')

        if request.FILES.get('property_image3'):
            data.image3 = request.FILES.get('property_image3')

        data.save()

        messages.success(request, "Property updated successfully!")

    return redirect(listed_properties)


def edit_property(request,pid):
    data=Property.objects.get(id=pid)
    obj=Property_type.objects.all()
    return render(request,'edit_property.html', {'data': data,'obj': obj})
def delete_property(request,pid):
    data=Property.objects.get(id=pid)
    data.delete()
    return redirect(listed_properties)



def filter_property(request):
    results = Property.objects.all()
    data = Property_type.objects.all()

    if request.method == "POST":

        location = request.POST.get('location')
        property_type = request.POST.get('type')
        price = request.POST.get('price')

        # 🔎 Keyword filter
        if location:
            results = results.filter(
                Q(property_title__icontains=location) |
                Q(location__icontains=location)
            )

        # 🏷 Type filter
        if property_type and property_type != "all":
            results = results.filter(property_type=property_type)

        # 💰 Price filter
        if price:
            if price and   price != '9999999':
                results = results.filter(price__lte=price)

    return render(request, 'filter_property.html', {
        'result': results,
        'data': data
    })







def enquiry_details(request,pid):
    if request.method == "POST":

        name = request.POST.get("name")
        mobile = request.POST.get("mobile")
        property_id = request.POST.get("id")
        property_title = request.POST.get("property")
        message = request.POST.get("message")

        Enquiry.objects.create(
            name=name,
            phone=mobile,
            property_id=property_id,
            property_title=property_title,
            message=message
        )

        messages.success(request,'message sent succesfully')   # change to your page

    return redirect('single_page',pid=pid)

def filter_id(request):

    if request.method =='POST':
        result=Property.objects.filter(property_id=request.POST.get('id'))
    return render(request,'filter_id.html',{'result':result})
def property_filter(request):
    properties = Property.objects.all()
    type=Property_type.objects.all()

    if request.method == "POST":
        place = request.POST.get('place')
        property_type = request.POST.get('type')
        price = request.POST.get('price')

        # Keyword filter (search in multiple fields)
        if place:
            properties = properties.filter(
                Q(property_title__icontains=place) |
                Q(location__icontains=place)
            )

        # Type filter
        if property_type and property_type != "all":
            properties = properties.filter(property_type=property_type)

        # Price filter
        if price and price != '99999999':
            properties = properties.filter(price__lte=price)

    return render(request, 'property_filter.html', {
        'properties': properties,'type':type
    })


def logout_view(request):
    # This removes the user ID from the session and deletes the session cookie
    logout(request)

    # Optional: Add a success message
    messages.info(request, "You have successfully logged out.")

    # Redirect to login page or home page
    return redirect('login')