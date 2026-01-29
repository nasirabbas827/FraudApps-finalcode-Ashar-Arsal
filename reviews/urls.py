from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Public
    path('', views.index, name='index'),                    # Landing page
    path('app/<int:app_id>/', views.app_detail, name='app_detail'),
    
    # Auth
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # User area
    path('dashboard/', views.dashboard, name='dashboard'),
    path('app/<int:app_id>/add-review/', views.add_review, name='add_review'),
    path('feedback/submit/', views.submit_feedback, name='submit_feedback'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
