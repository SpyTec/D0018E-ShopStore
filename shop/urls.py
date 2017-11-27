from django.conf.urls import url
from django.http import HttpResponse

from shop import views

urlpatterns = [
    url(r'^$', views.Overview.as_view(), name='shop'),
    url(r'checkout/$', views.checkout, name='shop_checkout'),
    url(r'product/(?P<pk>[0-9]+)/$', views.ProductView.as_view(), name='shop_detail'),
    url(r'product/(?P<pk>[0-9]+)/add_to_cart/$', views.add_to_cart, name='shop_add_to_cart'),
    url(r'category/$', views.CategoryOverview.as_view(), name='shop_category_overview'),
    url(r'category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='shop_category'),
]
