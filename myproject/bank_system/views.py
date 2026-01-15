from django.shortcuts import render,redirect,get_object_or_404
from bank.forms import RegisterForm,LoginForm,UserUpdateForm,BranchForm
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from django.urls import reverse
from bank_system.models import Branch
from bank.models import Register
#this function check the role of the user...
@login_required
def branch_redirect(request):
    profile = Profile.objects.get(user=request.user)

    # Redirect based on role
    if profile.role == 'admin':
        return redirect('admin_dashboard')
    elif profile.role == 'manager':
        return redirect('manager_dashboard')
    elif profile.role == 'customer':
        return redirect('customer_dashboard')
    else:
        return redirect('index')

# Admin dashboard
@login_required
def admin_dashboard(request):
    section = request.GET.get('section', 'customers')

    customers = Profile.objects.filter(role='customer').select_related('user', 'branch')
    managers = Profile.objects.filter(role='manager').select_related('user', 'branch')
    branches = Branch.objects.all()

    if request.method == "POST":
        profile_id = request.POST.get("profile_id")
        new_role = request.POST.get("role")
        new_branch_id = request.POST.get("branch")

        profile = Profile.objects.get(id=profile_id)

        # update role
        if new_role and new_role in ['customer', 'manager']:
            profile.role = new_role

        # update branch
        if new_branch_id:
            profile.branch_id = new_branch_id

        profile.save()
        return redirect(f"{reverse('admin_dashboard')}?section={section}")

    context = {
        "customers": customers,
        "managers": managers,
        "branches": branches,
        "section": section,
    }
    return render(request, "admin/dashboard.html", context)
#it will display the manager dashboard 
@login_required
def manager_dashboard(request):
    if not request.user.accounts_profile.role == 'manager':
        return redirect('login')  
    manager_branch = request.user.accounts_profile.branch
    total_customers = Profile.objects.filter(role='customer',branch=manager_branch).count()
    total_branches = Branch.objects.count()
    customers = Profile.objects.filter(role='customer',branch=manager_branch).select_related('user', 'branch')
    msg = request.user.accounts_profile.Message
    context = {

        'total_customers': total_customers,
        'total_branches': total_branches,
        'customers': customers,
        'message': msg,
    }
    return render(request, 'manager/dashboard.html', context)

#this method used for update the balance of user


#it is used for give the response to the customer
@login_required
def response(request, customer_id):
    manager = request.user.accounts_profile
    if manager.role != 'manager':
        return redirect('login')
    customer = get_object_or_404(Profile,id=customer_id,branch=manager.branch,role='customer')

    if request.method == 'POST':
        response_text = request.POST.get('res')
        customer.Response = response_text
        customer.save()
        return redirect('manager_dashboard')

    context = {
        'customer': customer,
        'manager': manager,
    }
    return render(request, 'manager/response.html', context)


def add_branch(request):
    if request.method == 'POST':
        form = BranchForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Branch added successfully!")
            return redirect('admin_dashboard')  # Replace with your branch listing URL name
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = BranchForm()  # Empty form for GET request


    return render(request, 'admin/addbranch.html',{'form': form})
