from django.urls import path
from bank_system import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin_dashboard/',views.admin_dashboard,name='admin_dashboard'),
    path('manager/',views.manager_dashboard,name='manager_dashboard'),
    path('redirect/',views.branch_redirect,name='branch_redirect'),
    path('approve_disable/<int:profile_id>/', views.approve_disable_request,name='approve_disable_request'),

    path('customer/response/<int:customer_id>/', views.response, name='response'),
    path('add_branch/',views.add_branch,name='add_branch'),
]

    
    

