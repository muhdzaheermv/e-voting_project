from . import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    # path('admin/', admin.site.urls),
   path('',views.index,name='index'),
   path('index/',views.index,name='index'),  
   
   path('register/',views.register,name='register'), 
   path('login/',views.login,name='login'),
   
   path('officer_register/',views.officer_register,name='officer_register'),
   path('officer_login/',views.officer_login,name='officer_login'),
   
]