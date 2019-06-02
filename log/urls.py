from django.urls import path
from .views import (
    sign_in_view,
    sign_up_view,
    logout_view,
    list_view,
    user_detail_view,
)


urlpatterns = [
    path('', sign_in_view),
    path('sign-in', sign_in_view),
    path('sign-up', sign_up_view),
    path('logout', logout_view),
    path('list', list_view),
    path('user-detail/<str:user_name>', user_detail_view),
]
