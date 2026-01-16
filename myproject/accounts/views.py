from django.shortcuts import render,redirect
from bank.forms import RegisterForm,LoginForm
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from bank.models import Register
from django.contrib.auth import login as auth_login
from django.http import JsonResponse
import qrcode
import io
import base64

#display the home page 
def index(request):
    return render(request,'index.html')

#display register form
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            # Hash password
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Create profile with role = customer
            Profile.objects.create(
                user=user,
                branch=form.cleaned_data['branch'],
                role='customer'
            )

            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

#display login form
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)  # Log the user in

                # Redirect based on profile role
                try:
                    profile = Profile.objects.get(user=user)
                except Profile.DoesNotExist:
                    messages.error(request, "Profile not found for this user.")
                    return redirect('index')

                if profile. role == 'customer':
                    return redirect('customer_dashboard')
                else:
                    return redirect('branch_redirect')
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

#it will display the customer dashboard 


@login_required
def customer_dashboard(request):
    customer_profile = request.user.accounts_profile
    manager_profile = Profile.objects.filter(branch=customer_profile.branch, role='manager').first()
    res = customer_profile.Response

    # Get account
    account = Register.objects.filter(user=customer_profile.user).first()
    acc = account.account_num 
    upi_id = account.upi_id 

    # Generate UPI ID if button clicked
    if request.GET.get('generate_upi') == '1' and account and not account.upi_id:
        # Format: username@bankname.ybi
        bank_name = customer_profile.branch.name.replace(" ", "").lower()  # remove spaces, lowercase
        generated_upi = f"{customer_profile.user.username.lower()}@{bank_name}.ybi"
        account.upi_id = generated_upi
        account.save()
        upi_id = generated_upi

    # QR Code logic
    show_qr = request.GET.get('show_qr') == '1'
    qr_image_base64 = None
    if show_qr:
        username = customer_profile.user.username
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(username)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        qr_image_base64 = base64.b64encode(buffer.getvalue()).decode()

    context = {
        'Response': res,
        'customer': customer_profile,
        'manager': manager_profile,
        'show_qr': show_qr,
        'qr_image_base64': qr_image_base64,
        'account': acc,
        'upi_id': upi_id,
    }

    return render(request, 'customer/dashboard.html', context)



#it will display the information of manger for contact the manager and send message to the user
@login_required
def contact(request):
   
    customer_profile = request.user.accounts_profile  # the logged-in user

    # Get the manager of the same branch
    manager_profile = Profile.objects.filter(branch=customer_profile.branch, role='manager').first()

    if request.method == 'POST':
        msg = request.POST.get('msg')
        customer_profile.Message = msg  # store the message in the logged-in user's profile
        customer_profile.save()
        return redirect('customer_dashboard')  # redirect after saving

    context = {
        'customer': customer_profile,
        'manager': manager_profile,
    }
    return render(request, 'customer/contact.html', context)

@login_required
def disable_req(request):
     customer_profile = request.user.accounts_profile
     if customer_profile.disable_request != "disable account":
        customer_profile.disable_request = "disable account"
        customer_profile.save()
     return redirect('index')




def loan_calculator(request):
    # Get values from GET parameters (default values if not provided)
    principal = float(request.GET.get('amount', 10000))
    interest = float(request.GET.get('interest', 10))
    years = float(request.GET.get('years', 5))

    # Calculate total interest and total payment
    total_interest = (principal * interest * years) / 100
    total_payment = principal + total_interest

    # Check if it's an AJAX request
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'total_interest': int(total_interest),
            'total_payment': int(total_payment)
        })

    # Regular page render
    context = {
        'principal': principal,
        'interest': interest,
        'years': years,
        'total_interest': total_interest,
        'total_payment': total_payment
    }
    return render(request, 'loan.html', context)