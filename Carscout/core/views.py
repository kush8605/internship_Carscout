# views.py
from django.shortcuts import render, redirect
from .forms import UserSignupForm, userlogin
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
import threading
import random
import datetime
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import os


def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp_email(email, otp, first_name):
    subject = 'WheelDeal - Login OTP Verification'
    from_email = settings.EMAIL_HOST_USER
    to = [email]

    html_content = render_to_string(
        'core/otp_email.html',
        {
            'otp': otp,
            'first_name': first_name,
        }
    )

    email_message = EmailMultiAlternatives(subject, '', from_email, to)
    email_message.attach_alternative(html_content, 'text/html')
    email_message.send()


def userSignupView(request):
    signup_form = UserSignupForm(request.POST or None)
    login_form = userlogin()

    if request.method == "POST":
        if signup_form.is_valid():
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
    signup_form = UserSignupForm()

    if request.method == 'POST':

        # ── OTP SUBMIT ──
        if request.POST.get('otp_submit'):
            digits = [
                request.POST.get('otp_1', ''),
                request.POST.get('otp_2', ''),
                request.POST.get('otp_3', ''),
                request.POST.get('otp_4', ''),
                request.POST.get('otp_5', ''),
                request.POST.get('otp_6', ''),
            ]
            entered_otp = ''.join(digits)
            session_otp = request.session.get('otp')
            expiry_str = request.session.get('otp_expiry')
            email = request.session.get('otp_email')

            if not email or not session_otp:
                return redirect('login')

            expiry = datetime.datetime.fromisoformat(expiry_str)
            if datetime.datetime.now() > expiry:
                return render(request, 'core/login.html', {
                    'signup_form': signup_form,
                    'login_form': login_form,
                    'show_verify_popup': True,
                    'verify_email': email,
                    'otp_error': 'OTP has expired. Please login again.',
                })

            if entered_otp == session_otp:
                from .models import User
                user = User.objects.get(email=email)
                user.status = 'active'
                user.save()

                del request.session['otp']
                del request.session['otp_email']
                del request.session['otp_expiry']

                login(request, user)

                if user.role == "Admin":
                    return redirect("adminhome")
                elif user.role == "Seller":
                    return redirect("sellerhome")
                elif user.role == "Buyer":
                    return redirect("buyerhome")
            else:
                return render(request, 'core/login.html', {
                    'signup_form': signup_form,
                    'login_form': login_form,
                    'show_verify_popup': True,
                    'verify_email': email,
                    'otp_error': 'Invalid OTP. Please try again.',
                })

        # ── RESEND OTP ──
        elif request.POST.get('resend_otp'):
            email = request.POST.get('resend_email')
            from .models import User
            try:
                user = User.objects.get(email=email)
                otp = generate_otp()
                request.session['otp'] = otp
                request.session['otp_email'] = email
                request.session['otp_expiry'] = str(
                    datetime.datetime.now() +
                    datetime.timedelta(minutes=5)
                )
                threading.Thread(
                    target=send_otp_email,
                    args=(email, otp, user.first_name),
                    daemon=True
                ).start()
            except User.DoesNotExist:
                pass
            return render(request, 'core/login.html', {
                'signup_form': signup_form,
                'login_form': login_form,
                'show_verify_popup': True,
                'verify_email': email,
                'otp_error': 'A new OTP has been sent to your email.',
            })

        # ── NORMAL LOGIN ──
        elif login_form.is_valid():
            email = login_form.cleaned_data['email']
            password = login_form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)

            if user is not None:
                if user.status == 'blocked':
                    login_form.add_error(None, "Your account has been blocked. Contact support.")
                elif user.status == 'deleted':
                    login_form.add_error(None, "Account not found.")
                elif user.status == 'active':
                    login(request, user)
                    if user.role == "Admin":
                        return redirect("adminhome")
                    elif user.role == "Seller":
                        return redirect("sellerhome")
                    elif user.role == "Buyer":
                        return redirect("buyerhome")
                elif user.status == 'inactive':
                    otp = generate_otp()
                    request.session['otp'] = otp
                    request.session['otp_email'] = email
                    request.session['otp_expiry'] = str(
                        datetime.datetime.now() +
                        datetime.timedelta(minutes=5)
                    )
                    threading.Thread(
                        target=send_otp_email,
                        args=(email, otp, user.first_name),
                        daemon=True
                    ).start()
                    return render(request, 'core/login.html', {
                        'signup_form': signup_form,
                        'login_form': login_form,
                        'show_verify_popup': True,
                        'verify_email': email,
                    })
            else:
                login_form.add_error(None, "Invalid email or password")

    return render(request, 'core/login.html', {
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