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
   path('officer_home/',views.officer_home,name='officer_home'),
   

   path('create_election/',views.create_election,name='create_election'),
   path('election_list/',views.election_list,name='election_list'),
   path('delete_election/<int:election_id>/', views.delete_election, name='delete_election'),
   
    path('create_election/', views.create_election, name='create_election'),
    path('create_candidate/<int:election_id>/', views.create_candidate, name='create_candidate'),
    path('edit_candidate/<int:candidate_id>/', views.edit_candidate, name='edit_candidate'),
    path('delete_candidate/<int:candidate_id>/', views.delete_candidate, name='delete_candidate'),
    path('election/<int:election_id>/view_candidates/', views.view_candidates, name='view_candidates'),
    
    
    
    path('election/<int:election_id>/edit/', views.edit_election, name='edit_election'),
    
    path('election/<int:id>/', views.election_details, name='election_details'),
   

   
]