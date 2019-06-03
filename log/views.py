# from django.http import Http404
from django.shortcuts import render, redirect  # , get_object_or_404, redirect
# from django.http import HttpResponseRedirect

from .forms import LogUserModelForm, LogUserModelFormm, GroupModelForm
from .models import LogUser, Group


def user_detail_view(request, user_name):
    user = LogUser.objects.get(user_name=user_name)
    context = {"title": "User Detail",
               'user': user, 'groups': ['assef', 'ahmad']}
    template_name = 'log/user-detail.html'
    return render(request, template_name, context)


def sign_in_view(request):
    form = LogUserModelFormm(request.POST or None)
    if form.is_valid():
        try:
            user_name = form.data['user_name']
            password = form.data['password']
            user = LogUser.objects.get(user_name=user_name, password=password)
            return redirect(user_detail_view, user_name=user_name)
        except:
            template_name = 'log/sign-in.html'
            context = {'form': form, "title": "SignIn Error"}
            return render(request, template_name, context)
    template_name = 'log/sign-in.html'
    context = {'form': form, "title": "SignIn"}
    return render(request, template_name, context)


def sign_up_view(request):
    form = LogUserModelForm(request.POST or None)
    if form.is_valid():
        form.save()
        # obj.user = request.user
        # obj.save()
        form = LogUserModelForm()
    template_name = 'log/sign-up.html'
    context = {'form': form, 'title': 'SignUp'}
    return render(request, template_name, context)


def logout_view(request): 
    template_name = 'log/luser_nameogout.html'
    context = {'title': 'Luser_nameogout'}
    return render(request, template_name, context)


def list_view(request):
    user_list = LogUser.objects.all()
    template_name = 'log/list.html'
    context = {'user_list': user_list, 'title': 'Logout'}
    return render(request, template_name, context)


def add_group_view(request, user_name):
    form = GroupModelForm(request.POST or None)
    if form.is_valid():
        try:
            print(form.data['group_name'])
            # group = Group.objects.create(group_name=form.group_name, admin=user_name)

        except:
            print('fuck')
    template_name = 'log/add-group.html'
    context = {'form': form, "title": "Add New Group"}
    return render(request, template_name, context)
