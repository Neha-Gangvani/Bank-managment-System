from django.contrib.auth import views as auth_views
from django.urls import path,include
from statement import views
urlpatterns = [
   path('update_bal/<int:customer_id>/',views.manager_update_customer,name='update_bal'),
     path('dashboard/',views.customer_statement, name='customer_statement'),
]