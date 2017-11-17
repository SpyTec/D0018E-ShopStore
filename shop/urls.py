from django.conf.urls import url
from django.http import HttpResponse

from shop import views

urlpatterns = [
    url(r'^$', views.Overview.as_view(), name='shop'),
    url(r'product/(?P<pk>[0-9]+)/$', views.ProductView.as_view(), name='shop_detail'),
    url(r'category/$', views.CategoryOverview.as_view(), name='shop_category_overview'),
    url(r'category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='shop_category'),
    url(r'cart/', lambda request: HttpResponse("Cart here", content_type="text/plain")),
]
