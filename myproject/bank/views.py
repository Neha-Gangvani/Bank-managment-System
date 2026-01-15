from django.shortcuts import render,redirect
from bank.forms import RegisterForm,LoginForm,UserUpdateForm,RegisterUpdateForm
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout
from bank.models import Register
from django.contrib.auth.decorators import login_required
def index(request):
    return render(request,'index.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('index')  # Redirect after successful login
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def dashboard(request):
     return render(request,'dashboard.html')
@login_required
def profile(request):
    # Ensure the user has a linked Register object
    register, created = Register.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        register_form = RegisterUpdateForm(
            request.POST, request.FILES, instance=register
        )

        if user_form.is_valid() and register_form.is_valid():
            user_form.save()
            register_form.save()
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        register_form = RegisterUpdateForm(instance=register)

    context = {
        'user_form': user_form,
        'register_form': register_form,
    }
    return render(request, 'profile.html', context)



def custom_logout(request):
    logout(request)
    return redirect('index')

