from django.conf.urls import url
from django.urls import reverse_lazy

from profile import views
from django.contrib.auth import views as admin

urlpatterns = [
    url(r'^$', views.Overview.as_view(), name="profile"),
    url(r'orders/$', views.Orders.as_view(), name="profile_orders"),
    # Authentication
    url(r'^login/$', admin.LoginView.as_view(), name='login'),
    url(r'^logout/$', admin.LogoutView.as_view(), name='logout'),
    url(r'^password_change/$', views.PasswordChangeWithMessageView.as_view(success_url=reverse_lazy('profile')),
        name='password_change'),
    # url(r'^password_change/done/$', admin.PasswordChangeDoneView.as_view(), name='password_change_done'),

    url(r'^register/$', views.RegistrationView.as_view(), name='registration_register'),
    url(r'^edit/$', views.ProfileEditView.as_view(), name='edit_profile'),
    # url(r'^cart/$', views.UserCart.as_view(), name='profile_cart'),
    url(r'^cart/$', views.user_cart, name='profile_cart'),
    # url(r'^cart/update/$', views.UpdateUserCart.as_view(), name='profile_cart_update'),
]
