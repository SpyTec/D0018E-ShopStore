from django.conf.urls import url

from shop import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='shop'),
    url(r'(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='shop_detail'),
]
