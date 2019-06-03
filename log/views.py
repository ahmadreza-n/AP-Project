# from django.contrib.auth.decorators import login_required
# from django.contrib.admin.views.decorators import staff_member_required
# from django.http import Http404
from django.shortcuts import render, redirect  # , get_object_or_404, redirect
# from django.http import HttpResponseRedirect

from .forms import LogUserModelForm, LogUserModelFormm, GroupModelForm
from .models import LogUser, Group


# Create your views here.


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
# def blog_post_list_view(request):
#     # list out objects
#     # could be search
#     # queryset -> list of python object
#     qs = BlogPost.objects.all().published()
#     if request.user.is_authenticated:
#         my_qs = BlogPost.objects.filter(user=request.user)
#         qs = (qs | my_qs).distinct()
#     template_name = 'blog/list.html'
#     context = {'object_list': qs}
#     return render(request, template_name, context)


# # @login_required
# @staff_member_required
# def blog_post_create_view(request):
#     # create objects
#     # ? use a form
#     # request.user -> return something
#     form = BlogPostModelForm(request.POST or None, request.FILES or None)
#     if form.is_valid():
#         obj = form.save(commit=False)
#         obj.user = request.user
#         obj.save()
#         form = BlogPostModelForm()
#     template_name = 'form.models.CASCADEhtml'
#     context = {'form': form}
#     return render(request, template_name, context)


# def blog_post_detail_view(request, slug):
#     # 1 object -> detail view
#     obj = get_object_or_404(BlogPost, slug=slug)
#     template_name = 'blog/detail.html'
#     context = {"object": obj}
#     return render(request, template_name, context)

# @staff_member_required
# def blog_post_update_view(request, slug):
#     obj = get_object_or_404(BlogPost, slug=slug)
#     form = BlogPostModelForm(request.POST or None, instance=obj)
#     if form.is_valid():
#         form.save()
#     template_name = 'form.html'
#     context = {"title": f"Update {obj.title}", "form": form}
#     return render(request, template_name, context)


# @staff_member_required
# def blog_post_delete_view(request, slug):
#     obj = get_object_or_404(BlogPost, slug=slug)
#     template_name = 'blog/delete.html'
#     if request.method == "POST":
#         obj.delete()
#         return redirect("/blog")
#     context = {"object": obj}
#     return render(request, template_name, context)
