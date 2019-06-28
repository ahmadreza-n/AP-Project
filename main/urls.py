from django.urls import path


from . import views


urlpatterns = [
     path('', views.home_view),
     path('about', views.about_view),
     path('contact', views.contact_view),
     path('login', views.login_view),
     path('register', views.register_view),
     path('logout', views.logout_view),
     # path('list', views.list_view),
     path('<slug:username>', views.account_view),
     path('<slug:username>/add-group', views.add_group_view),
     path('<slug:username>/<slug:group_id>', views.group_view),
     path('<slug:username>/<slug:group_id>/add-expense',
          views.add_expense_view),
     path('<slug:username>/<slug:group_id>/delete-group',
          views.delete_group_view),
     path('<slug:username>/<slug:group_id>/edit-group',
          views.edit_group_view),
     path('<slug:username>/<slug:group_id>/settle/<slug:settler_id>',
          views.settle_view),
     path('<slug:username>/<slug:group_id>/<int:expense_pk>',
          views.expense_view),
]
