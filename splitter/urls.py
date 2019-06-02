from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include
from blog.views import (
    blog_post_create_view,
)

from searches.views import search_view
from .views import (
    home_page,
    about_page,
    contact_page,
    example_page
)

urlpatterns = [
    path('', home_page),
    path('blog-new/', blog_post_create_view),
    path('blog/', include('blog.urls')),
    path('log/', include('log.urls')),
    path('search/', search_view),
    path('page/', about_page),
    path('pages/', about_page),
    re_path(r'^pages?/$', about_page),
    re_path(r'^about/$', about_page),
    path('example/', example_page),
    path('contact/', contact_page),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)






