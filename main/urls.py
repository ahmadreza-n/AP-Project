from django.contrib import admin
from django.urls import path


from . import views


urlpatterns = [
    path('', views.home_page),
    path('about/', views.about_page),
    path('contact/', views.contact_page),
    path('sign-in', views.sign_in_view),
    path('sign-up', views.sign_up_view),
    path('sign-out', views.sign_out_view),
    path('list', views.list_view),
    path('<str:user_name>', views.user_detail_view),
    path('add-group/<str:user_name>', views.add_group_view),
]
