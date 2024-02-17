
from django.shortcuts import render,HttpResponse,redirect
from .models import Booking
from django.contrib.auth.models import User
from django.contrib.auth import logout as django_logout
import random
from django.http import Http404
from django.core.exceptions import PermissionDenied

from django.utils.crypto import get_random_string
from xhtml2pdf import pisa
from django.template.loader import get_template
from .utils import check_internet_connection
import requests
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
def faq(request):
    return render(request ,'faq.html')
def about(request):
    return render(request,'about.html')
def error_handler(request, exception):
    if isinstance(exception, Http404):
        status = 404
    elif isinstance(exception, PermissionDenied):
        status = 403
    else:
        status = 500

    return render(request, '404.html', {'status': status})


def generate_pdf(request, tracking_id, sender_name, receiver_name, pickup_address, delivery_address, package_description):
    html_string = get_template('receipt.html').render({
        'tracking_id': tracking_id,
        'sender_name': sender_name,
        'receiver_name': receiver_name,
        'pickup_address': pickup_address,
        'delivery_address': delivery_address,
        'package_description': package_description
    })

    # Set the desired file name using tracking_id
    pdf_filename = f"{tracking_id}.pdf"

    # Create a PDF file
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{pdf_filename}"'

    # Generate PDF
    pisa_status = pisa.CreatePDF(html_string, dest=response)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html_string + '</pre>')

    return response
generated_tracking_numbers = set()
def track_bookings(request):
    # if not check_internet_connection():
    #     return render(request,'404.html')
    tracking_id = request.GET.get('tracking_id')
    print("Received tracking ID:", tracking_id)
    user_bookings = Booking.objects.filter(tracking_id=tracking_id)
    if user_bookings.exists():
        message = None
    else:
        message = 'No bookings found for the given tracking ID.'
    return render(request, 'view_bookings.html', {'user_bookings': user_bookings, 'message': message})
@login_required
def view_bookings(request):
    isAuthenticated=True;
    username = request.user
    user_bookings = Booking.objects.filter(booking_user=username)
    if user_bookings.exists():
        message = None
    else:
        message = 'No bookings found for the given tracking ID.'
    return render(request, 'view_bookings.html', {'user_bookings': user_bookings, 'message': message,'isAuthenticated':True})

def generate_unique_random_number(length):

    while True:
        # Generate a random number with the specified length
        random_number = str(random.randint(10 ** (length - 1), 10 ** length - 1))

        # Ensure the generated number is unique
        if random_number not in generated_tracking_numbers:
            generated_tracking_numbers.add(random_number)
            return random_number
@login_required
def booking_confirm(request):
    if request.method == 'POST':
        recaptcha_response = request.POST.get('g-recaptcha-response')
        secret_key = '6Le0RJgoAAAAAGVPLP8z_zbyuQn-Kwyo4frr_t41'
        data = {
            'secret': secret_key,
            'response': recaptcha_response
        }
        response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = response.json()

        if not result['success']:
            return render(request, 'booking.html', {'message': 'Captcha Verification Failed'})
        booking_user = request.user
        sender_name = request.POST.get('sender_name')
        receiver_name = request.POST.get('receiver_name')
        pickup_address = request.POST.get('pickup_address')
        delivery_address = request.POST.get('delivery_address')
        package_description = request.POST.get('package_description')
        package_status="Booked"
        # Generate a unique tracking ID
        tracking_id = generate_unique_random_number(10)
        # Save the booking details to the database
        booking = Booking(
            booking_user=booking_user,
            sender_name=sender_name,
            receiver_name=receiver_name,
            pickup_address=pickup_address,
            delivery_address=delivery_address,
            package_description=package_description,
            tracking_id=tracking_id,
            Current_Status=package_status
        )
        booking.save()


        return render(request, 'receipt.html', {
            'tracking_id': tracking_id,
            'sender_name': sender_name,
            'receiver_name': receiver_name,
            'pickup_address': pickup_address,
            'delivery_address': delivery_address,
            'package_description': package_description,
            'isAuthenticated':True
        })
    else:
        return redirect('receipt')
def landing_page(request):

    isAuthenticated = request.user.is_authenticated
    return render(request,'landing.html',{'isAuthenticated':isAuthenticated})
def signup(request):

    # if not check_internet_connection():
    #     return render(request,'404.html')
    return render(request,'signup.html')
def login_page(request):
    # if not check_internet_connection():
    #     return render(request,'404.html')
    isAuthenticated = request.user.is_authenticated
    if (isAuthenticated):
        return redirect('/')
    else:
        return render(request,'login.html')
@login_required
def booking(request):
    isAuthenticated=True;
    username = request.user
    return render(request,'booking.html',{'username':username,'isAuthenticated':isAuthenticated})
@login_required
def logout(request):
    django_logout(request)
    return render(request, 'landing.html', {'message': 'Logged Out Successfully'})
def login_check(request):
    global username
    username = ''
    if request.method == "POST":
        recaptcha_response = request.POST.get('g-recaptcha-response')
        secret_key = '6Le0RJgoAAAAAGVPLP8z_zbyuQn-Kwyo4frr_t41'
        data = {
            'secret': secret_key,
            'response': recaptcha_response
        }
        response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = response.json()

        if not result['success']:
            return render(request, 'login.html', {'message': 'Captcha Verification Failed'})


        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_staff:
                    return render(request, 'login.html', {'message': 'Administrative user, please use the admin login portal for access.'})
                login(request, user)
                first_name = user.first_name
                return redirect('/dashboard')
            else:
                return render(request, 'login.html', {'message': 'Invalid UserName or Password.'})
        except User.DoesNotExist:
            return render(request, 'login.html', {'message': 'Invalid UserName or Password.'})
    return render(request, 'login.html')
@login_required
def dashboard(request):
    isAuthenticated=True
    user = request.user
    firstname= user.first_name
    return render(request, 'dashboard.html', {'user': user,'first_name':firstname ,'isAuthenticated': isAuthenticated})
# def register(request):
#     if not check_internet_connection():
#         return render(request,'404.html')
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         confpassword = request.POST['confirm_password']
#         firstname = request.POST['first_name']
#         lastname=request.POST['last_name']
#         email=request.POST['email']
#         if Info.objects.filter(username=username).exists():
#             return render(request,'signup.html',{'error':'Username Already Taken'})
#         if(password==confpassword):
#             user = Info(first_name=firstname, last_name=lastname,
#                         username=username, email=email, password=password)
#             user.save()
#             return render(request, 'login.html', {'message': 'User Created Successfully '})
#         else:
#             return render(request,'signup.html',{'error':'Password and Confirm Password Fields Must Match'})
#     return redirect('signup')
def register(request):

    if request.method == 'POST':
        recaptcha_response = request.POST.get('g-recaptcha-response')
        secret_key = '6Le0RJgoAAAAAGVPLP8z_zbyuQn-Kwyo4frr_t41'
        data = {
            'secret': secret_key,
            'response': recaptcha_response
        }
        response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = response.json()

        if not result['success']:
            return render(request, 'signup.html', {'error': 'Captcha Verification Failed'})
        username = request.POST['username']
        password = request.POST['password']
        confpassword = request.POST['confirm_password']
        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        email = request.POST['email']

        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username Already Taken'})
        if User.objects.filter(email=email).exists():
            return render(request,'signup.html',{'error':'Email Already Exists'})


        if password == confpassword:
            # Create a new user using Django's User model
            otp = generate_otp()

        # Send OTP via email
            send_otp_email(email, otp)

        # Add OTP to session for verification
            request.session['otp'] = otp
            request.session['user_data'] = {
                'username': username,
                'password': password,
                'confpassword': confpassword,
                'firstname': firstname,
                'lastname': lastname,
                'email': email,
            }

            return render(request, 'verify_otp.html', {'email': email})

        else:
            return render(request,'signup.html',{'error':'Password and Confirm Password Fields Must Match'})
    return redirect('signup')

def verify_otp(request):

    user_data = request.session.get('user_data', {})
    email = user_data.get('email', '')
    stored_otp = request.session.get('otp')

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')

        if stored_otp == entered_otp:
            username = user_data.get('username', '')
            password = user_data.get('password', '')
            firstname = user_data.get('firstname', '')
            lastname = user_data.get('lastname', '')


            user = User.objects.create_user(username, email, password)
            user.first_name = firstname
            user.last_name = lastname
            user.save()



            # Clear the session data
            request.session.pop('user_data', None)
            request.session.pop('otp', None)

            return render(request, 'login.html', {'message': 'User Created Successfully'})

        else:
            return render(request, 'verify_otp.html', {'email': email, 'error': 'Invalid OTP'})

    return render(request, 'verify_otp.html', {'email': email})



from django.shortcuts import redirect
from django.contrib.auth import logout as django_logout
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password
def forgot_password(request):
    return render(request,'forgot_password.html')
def send_otp_email(email, otp):
    subject = 'Swift Courier Account Verification '
    message = f'Your OTP for account verification on Swift Courier is: {otp}  Do not share it with anyone.'
    from_email = 'Swift Courier Company '+settings.EMAIL_HOST_USER
    send_mail(subject, message, from_email, [email])
def send_password_change_mail(email,name):
    subject = 'Swift Courier - Account Password Changed '
    message = f'Hi {name},\n Your Account Password Changed Successfully '
    from_email = 'Swift Courier Company '+settings.EMAIL_HOST_USER
    send_mail(subject, message, from_email, [email])
def custom_logout(request):
    # if not check_internet_connection():
    #     return render(request,'404.html')
    django_logout(request)
    return redirect('/')
def forgot_verify(request):

    if request.method =='POST':
        email = request.POST['email']
    if User.objects.filter(email=email).exists():
        otp = generate_otp()

        # Send OTP via email
        send_otp_email(email, otp)

        # Add OTP to session for verification
        request.session['otp_forgot'] = otp
        request.session['user_data_forgot'] = {
            'email': email,
        }
        return render(request,'verify_otp_forgot', {'email': email})
    else:
        return render(request,'forgot_password.html',{'message':'We can not find any account with the provided email'})



def generate_otp():
    return str(random.randint(100000, 999999))

def verify_otp_forgot(request):
    # if not check_internet_connection():
    #     return render(request, '404.html')
    user_data = request.session.get('user_data_forgot', {})
    email = user_data.get('email', '')
    stored_otp = request.session.get('otp_forgot')

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')

        if stored_otp == entered_otp:

            request.session.pop('otp', None)

            return render(request, 'change_password.html', {'message': 'Verification Successfull Create New Password'})

        else:
            return render(request, 'verify_otp_forgot', {'email': email, 'error': 'Invalid OTP entered'})

    return render(request, 'verify_otp_forgot', {'email': email})
def change_password(request):
    # if not check_internet_connection():
    #     return render(request, '404.html')
    user_data = request.session.get('user_data_forgot', {})
    email = user_data.get('email', '')
    name = user_data.get('first_name','')
    print(email)
    if request.method == 'POST':
        password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        print(password)
        if password==confirm_password:

            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            send_password_change_mail(email,name)

            return render(request,'login.html',{'message':'Password Successfully Changed'})
        else:
            return render(request,'change_password.html',{'message':'Password and Confirm Password should match'})
    return render(request,'login.html')

