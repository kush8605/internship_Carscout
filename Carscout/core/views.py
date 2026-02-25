from django.shortcuts import render, redirect
from .forms import UserSignupForm, userlogin
from django.contrib.auth import authenticate, login


def userSignupView(request):
    if request.method == "POST":
        form = UserSignupForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = UserSignupForm()

    return render(request, 'core/signup.html', {'form': form})





def userLoginView(request):
    if request.method == 'POST':
        form = userlogin(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)   # ✅ CORRECT

                if user.role == "Admin":
                    return redirect("adminhome")
                elif user.role == "Buyer":
                    return redirect("home")
            else:
                 return render(request, 'core/login.html', {'form': form})
    else:
        form = userlogin()
        return render(request, 'core/login.html', {'form': form})