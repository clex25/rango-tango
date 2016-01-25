from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from registration.backends.simple.views import RegistrationView

class MyRegistrationView(RegistrationView):
    def get_success_url(self, request, user):
        return '/rango/'

urlpatterns = [
    # Examples:
    # url(r'^$', 'tango_with_django_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^rango/', include('rango.urls')),
    url(r'^favicon.ico$', RedirectView.as_view(
                            url='static/favicon.ico')),
    url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    