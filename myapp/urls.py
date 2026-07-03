from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_page, name='about'),
    path('causes/', views.causes_page, name='causes'),
    path('donate/', views.donate_page, name='donate_page'),
    path('donate/success/', views.donate_success, name='donate_success'),
    path('contact/', views.contact_page, name='contact_page'),
    path('volunteer/', views.volunteer_page, name='volunteer_page'),
]
