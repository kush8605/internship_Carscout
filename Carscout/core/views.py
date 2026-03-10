# views.py
from django.shortcuts import render, redirect
from .forms import UserSignupForm, userlogin
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
import threading
from django.core.mail import  EmailMultiAlternatives
from django.template.loader import render_to_string
import os

def userSignupView(request):
    signup_form = UserSignupForm(request.POST or None)
    login_form = userlogin()  # empty login form for the left panel

    if request.method == "POST":
        
        if signup_form.is_valid():
            #email config
            email = signup_form.cleaned_data['email']
            user = signup_form.save()
            threading.Thread(
                target=send_welcome_email,
                args=(user,),
                daemon=True
            ).start()
            return redirect('login')

    return render(request, 'core/signup.html', {
        'signup_form': signup_form,
        'login_form': login_form,
    })


def userLoginView(request):
    login_form = userlogin(request.POST or None)
    signup_form = UserSignupForm()  # empty signup form for the right panel

    if request.method == 'POST':
        if login_form.is_valid():
            email = login_form.cleaned_data['email']
            password = login_form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                if user.role == "Admin":
                    return redirect("adminhome")
                elif user.role == "Seller":
                    return redirect("sellerhome")
                elif user.role == "Buyer":
                    return redirect("buyerhome")
            else:
                login_form.add_error(None, "Invalid email or password")

    return render(request, 'core/login.html',{
        'signup_form': signup_form,
        'login_form': login_form,
    })

def logoutview(request):
    logout(request)
    return redirect("homepage")

def send_welcome_email(user):
    subject = "Welcome to WheelDeal"
    from_email = settings.EMAIL_HOST_USER
    to = [user.email]

    html_content = render_to_string(
        "core/welcomeemail.html",
        {"first_name": user.first_name}
    )

    email_message = EmailMultiAlternatives(
        subject,
        "Welcome to WheelDeal",
        from_email,
        to
    )

    email_message.attach_alternative(html_content, "text/html")
    image_path = os.path.join(settings.BASE_DIR, 'static/images/welcome.png')
    email_message.attach_file(image_path)

    email_message.send()



    
