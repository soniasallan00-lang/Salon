from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),  
    path('index/', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('gallery/', views.gallery, name='gallery'),
    path('team/', views.team, name='team'),
    path('contact/', views.contact, name='contact'),
    path('booking/', views.booking, name='booking'),
    path('booking/payment/', views.booking_payment, name='booking_payment'),
    path('booking/confirm/', views.booking_confirm, name='booking_confirm'),
    path('salon-admin/', views.salon_admin, name='salon_admin'),
    path('salon-admin/booking/<int:booking_id>/<str:action>/', views.admin_booking_action, name='admin_booking_action'),
    path('sentmessage/', views.sentmessage, name='sentmessage'),
    path('request/', views.request_view, name='request'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    
]