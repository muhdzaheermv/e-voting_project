from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'vote'

urlpatterns = [
    path('', views.index, name='index'),  # Add the index page URL
    
    path('voter_register/', views.voter_registration, name='voter_registration'),
    path('voter_login/', views.voter_login, name='voter_login'),
    path('voter_logout/', views.voter_logout, name='voter_logout')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

