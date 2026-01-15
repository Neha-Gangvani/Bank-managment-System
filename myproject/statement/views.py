from django.shortcuts import render
from statement.models import Statement
from decimal import Decimal, InvalidOperation
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from django.contrib import messages

@login_required
def manager_update_customer(request, customer_id):
    # Check if user is a manager
    if not request.user.accounts_profile.role == 'manager':
        return redirect('login')

    # Get the customer in the same branch
    manager_branch = request.user.accounts_profile.branch
    try:
        customer = Profile.objects.get(id=customer_id, role='customer', branch=manager_branch)
    except Profile.DoesNotExist:
        messages.error(request, "Customer not found in your branch.")
        return redirect('manager_dashboard')

    if request.method == 'POST':
        bal = request.POST.get('bal')
        action = request.POST.get('action')  # 'credit' or 'deduct'

        if bal and action in ['credit', 'deduct']:
            try:
                amount = Decimal(bal)  # convert to Decimal

                if action == 'credit':
                    customer.bal += amount
                elif action == 'deduct':
                    customer.bal -= amount

                customer.save()

                # Create a Statement record
                Statement.objects.create(
                    user=customer.user,
                    bal=amount,
                    transaction_type=action
                )

                messages.success(request, f"{action.capitalize()} successful.")
                return redirect('manager_dashboard')

            except InvalidOperation:
                messages.error(request, "Invalid balance value.")
        else:
            messages.error(request, "Please provide a valid amount and action.")

    context = {'customer': customer}
    return render(request, 'manager/update.html', context)

@login_required

def customer_statement(request):
    statements = Statement.objects.filter(user=request.user).order_by('date')  # oldest first
    total_balance = 0
    statement_list = []

    for stmt in statements:
        # update running total
        if stmt.transaction_type == 'credit':
            total_balance += stmt.bal
        else:  # 'deduct'
            total_balance -= stmt.bal

        # append tuple of statement + total balance
        statement_list.append({
            'date': stmt.date,
            'transaction_type': stmt.transaction_type,
            'bal': stmt.bal,
            'total': total_balance
        })

    context = {
        'statements': statement_list
    }
    return render(request, 'customer/statement.html', context)
