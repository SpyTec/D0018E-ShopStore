from django.conf.urls import url
from django.http import HttpResponse

urlpatterns = [
    url(r'^checkout/', lambda request: HttpResponse("Checkout", content_type="text/plain")),
    url(r'^process/', lambda request: HttpResponse("Processing order", content_type="text/plain")),
    url(r'^(?P<pk>[0-9]+)/', lambda request: HttpResponse("Display your order", content_type="text/plain")),
]
