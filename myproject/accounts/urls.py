from django.urls import path
from accounts import views  # Make sure this line exists

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'), 
    path('loan/',views.loan_calculator,name='loan'),
     path('customer/',views.customer_dashboard,name='customer_dashboard'),
     path('contact/',views.contact,name='contact'),
]
