from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect

# Create your views here.
from .forms import LogUserModelForm, LogUserModelFormm
from .models import LogUser

def user_detail_view(request, user_name):
    template_name = 'log/user-detail.html'
    user = get_object_or_404(LogUser, user_name=user_name)
    context = {"title": "User Detail", 'user': user }
    return render(request, template_name, context)


def sign_in_view(request):
    form = LogUserModelFormm(request.POST or None)
    if form.is_valid():
        # obj.user = request.user
        # form = LogUserModelFormm()
        try:
            user_name = form.data['user_name']
            password = form.data['password']
            user = LogUser.objects.get(user_name=user_name, password=password)
            template_name = 'log/user-detail.html'
            context = {"title": "User Detail", 'user': user }
            return HttpResponseRedirect(f'user-detail/{user_name}')
            # return user_detail_view(request, user_name)
            # return render(request, template_name, context)
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
        obj = form.save()
        # obj.user = request.user
        # obj.save()
        form = LogUserModelForm()
    template_name = 'log/sign-up.html'
    context = {'form': form, 'title': 'SignUp'}
    return render(request, template_name, context)

def logout_view(request):
    template_name = 'log/logout.html'
    context = {'title': 'Logout'}
    return render(request, template_name, context)

def list_view(request):
    user_list = LogUser.objects.all()
    template_name = 'log/list.html'
    context = {'user_list': user_list, 'title': 'Logout'}
    return render(request, template_name, context)


# def blog_post_list_view(request):
#     # list out objects 
#     # could be search
#     qs = BlogPost.objects.all().published() # queryset -> list of python object
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
#     template_name = 'form.html'
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









