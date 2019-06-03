from django.urls import path
from . import views


urlpatterns = [
    path('', views.sign_in_view),
    path('sign-in', views.sign_in_view),
    path('sign-up', views.sign_up_view),
    path('logout', views.logout_view),
    path('list', views.list_view),
    path('user-detail/<str:user_name>', views.user_detail_view),
    path('add-group/<str:user_name>', views.add_group_view),
]
