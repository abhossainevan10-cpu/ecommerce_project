from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# রেজিস্ট্রেশন ভিউ
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

# লগইন ভিউ
def login_view(request):
    if request.method == 'POST':
        user_nm = request.POST.get('username')
        pass_wd = request.POST.get('password')

        user = authenticate(request, username=user_nm, password=pass_wd)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'accounts/login.html')

# লগআউট ভিউ
def logout_view(request):
    logout(request)
    return redirect('home')