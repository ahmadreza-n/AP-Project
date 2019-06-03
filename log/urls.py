from django.urls import path
from .views import *


urlpatterns = [
    path('', sign_in_view),
    path('sign-in', sign_in_view),
    path('sign-up', sign_up_view),
    path('logout', logout_view),
    path('list', list_view),
    path('user-detail/<str:user_name>', user_detail_view),
    path('add-group/<str:user_name>', add_group_view),
]
