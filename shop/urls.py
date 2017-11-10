from django.conf.urls import url

from shop import views

urlpatterns = [
    url(r'^', views.IndexView.as_view(), name='shop'),
]
