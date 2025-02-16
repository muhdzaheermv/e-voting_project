from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    # path('admin/', admin.site.urls),,
   path('',views.index,name='index'),
   path('about/',views.about,name='about'),
   path('guide/',views.guide,name='guide'),
   path('contact/',views.contact,name='contact'),

   path('index/',views.index,name='index'),  
   
   path('register/',views.register,name='register'), 
#    path('login/',views.login,name='login'),
   
   path('available_elections/', views.available_elections, name='available_elections'),
    path('vote/<int:election_id>/', views.vote, name='vote'),
    path('logout/', views.logout, name='logout'),
   
   path('officer_register/',views.officer_register,name='officer_register'),
   path('officer_login/',views.officer_login,name='officer_login'),
   path('officer_home/',views.officer_home,name='officer_home'),
   

   path('create_election/',views.create_election,name='create_election'),
   path('election_list/',views.election_list,name='election_list'),
   path('voters_list/',views.voters_list,name='voters_list'),
   path('delete_election/<int:election_id>/', views.delete_election, name='delete_election'),
   
   path('election/create/', views.create_election, name='create_election'),
    path('election/<int:election_id>/', views.election_detail, name='election_detail'),
    
    path('election_manager/<int:election_id>/', views.election_detail_manager, name='election_detail_manager'),
    # If you also have an edit page, you can define it separately:
    path('election/<int:election_id>/edit/', views.edit_election, name='edit_election'),
   
    path('create_election/', views.create_election, name='create_election'),
    path('create_candidate/<int:election_id>/', views.create_candidate, name='create_candidate'),
    path('edit_candidate/<int:candidate_id>/', views.edit_candidate, name='edit_candidate'),
    path('delete_candidate/<int:candidate_id>/', views.delete_candidate, name='delete_candidate'),
    path('election/<int:election_id>/view_candidates/', views.view_candidates, name='view_candidates'),
    
    
    
    path('election/<int:election_id>/edit/', views.edit_election, name='edit_election'),
    
    
    
    
    path('result/<int:election_id>/', views.election_result, name='election_result'),
    
    path('voters/<int:election_id>/', views.voter_list, name='voter_list'),
    
    path('add_eligible_voter/<int:election_id>/', views.add_eligible_voter, name='add_eligible_voter'),
    path('edit_eligible_voter/<int:eligible_voter_id>/', views.edit_eligible_voter, name='edit_eligible_voter'),
    path('delete_eligible_voter/<int:eligible_voter_id>/', views.delete_eligible_voter, name='delete_eligible_voter'),
    
    path('eligible_voter_list/<int:election_id>/', views.eligible_voter_list, name='eligible_voter_list'),
    
    path('election/<int:election_id>/eligible_voters/', views.eligible_voter_list, name='eligible_voters'),
    
    path('manager/register/', views.register_manager, name='register_manager'),
    path('manager/login/', views.login_manager, name='login_manager'),
    path('manager/dashboard/', views.manager_dashboard, name='manager_dashboard'),
    
    path('presiding_officer/register/', views.register_presiding_officer, name='register_presiding_officer'),
    path('presiding_officer/login/', views.login_presiding_officer, name='login_presiding_officer'),
    path('presiding_officer/dashboard/', views.presiding_officer_dashboard, name='presiding_officer_dashboard'),
    
    # path('voter/verify/', views.voter_verify, name='voter_verify'),
    path('voter/verify/', views.verify_voters, name='verify_voters'),
    path('upload-voters/', views.upload_voters, name='upload_voters'),
    path('voter/login/', views.voter_login, name='voter_login'),
    path('voter/verify/', views.verify_voters, name='verify_voters'),
    # path('vote/<int:election_id>/', views.vote, name='vote'),
    
    path('upload-success/', views.upload_success, name='upload_success'),
    
    path('candidate/login/', views.candidate_login, name='candidate_login'),
    path('vote/<int:election_id>/<str:voter_id>/', views.vote, name='vote'),
    path('campaign/', views.campaign, name='campaign'),
    
    path("elections/", views.list_elections, name="elections"),
    path("elections/create/", views.create_election, name="create_election"),
    path("candidates/", views.list_candidates, name="candidates"),
    path("candidates/add/", views.add_candidate, name="add_candidate"),
    
     
     
    
   

   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)