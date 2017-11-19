from django.conf.urls import url, include

from profile import views
from profile.views import RegistrationView

urlpatterns = [
    url(r'^$', views.Overview.as_view(), name="profile"),
    url(r'orders/$', views.Orders.as_view(), name="profile_orders"),
    # Authentication
    url('^', include('django.contrib.auth.urls')),
    url(r'^register/$', RegistrationView.as_view(), name='registration_register'),
]
