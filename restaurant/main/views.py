from django.shortcuts import render,redirect
from .models import Customer, Management
from django.core.mail import EmailMessage,send_mail
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
# Create your views here.
def index(request):
    buff=Management.objects.filter(category='buff')
    veg=Management.objects.filter(category='veg')
    chicken=Management.objects.filter(category='chicken')

    return render(request,'main/index.html',{'buff':buff,'veg':veg,'chicken':chicken})
def about(request):
    return render(request, 'main/about.html')
def contact(request):
    return render(request, 'main/contact.html')
@login_required(login_url="login")
def menu(request):
    return render(request, 'main/menu.html')
def service(request):
    return render(request, 'main/services.html')
def customer(request):
    if request.method=='POST':
        data=request.POST
        name=data['name']
        email=data['email']
        phonenumber=data['phonenumber']
        msg=data['message']
        Customer.objects.create(name=name,email=email,phonenumber=phonenumber,message=msg)

        subject="Thankyou for your message"
        message=render_to_string('main/message.html',{'name':name})
        from_email="sampadashrestha435@gmail.com"
        recipient_list=[email]
        send_mail(subject,message,from_email,recipient_list, fail_silently=True)
        msg_email=EmailMessage(subject,message,from_email,recipient_list)
        msg_email.send(fail_silently=True)
    return redirect('index')



# authorization



def register(request):
    if request.method=="POST":
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        email=request.POST['email']
        username=request.POST['username']
        password=request.POST['password']
        password1=request.POST['password1']

        if password==password1:
            try:
                validate_password(password)
                if User.objects.filter(username=username).exists():
                    messages.error(request,'This username already exists')
                    return redirect('register')
                elif User.objects.filter(email=email).exists():
                    messages.error(request,'This email already has an account')
                    return redirect('register')
                else:
                    User.objects.create_user(first_name=firstname,last_name=lastname,email=email,username=username,password=password)
                    messages.success(request,"Registered successfully")
                    return redirect('login')
            except ValidationError as e:
                for error in e.messages:
                    messages.error(request,error)
                    return redirect('register')
        else:
            messages.error(request,"Your password and confirm passwords do not match")
            return redirect('register')
    return render(request, 'auth/register.html')
def log_in(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        remember_me = request.POST.get('remember_me')

        if not User.objects.filter(username=username):
            messages.error(request,"Username does not exist")
            return redirect('login')
        else:
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                if remember_me:
                    request.session.set_expiry(12000000)
                else:
                    request.session.set_expiry(0)
                messages.success(request,"login successful")
                return redirect('index')
            else:
                messages.error(request,"Incorrect Password")
                return redirect('login')
    return render(request,'auth/login.html')
def log_out(request):
    logout(request)
    return redirect('login')

@login_required(login_url='log_in')
def change_password(request):
    form=PasswordChangeForm(user=request.user)
    if request.method=="POST":
        form=PasswordChangeForm(user=request.user,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(request,'auth/changepassword.html',{'form':form})