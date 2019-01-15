from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import serializers, viewsets, routers
from rest_framework.urlpatterns import format_suffix_patterns

from api.views import (
    LoginAPIView,
    IntrospectAPIView,
    RegisterAPIView,
    UserListCreateAPIView,
    UserRetrieveUpdateDestroyAPIView
)


urlpatterns = [
    url(r'^api/login$', LoginAPIView.as_view(), name='mikaid_login_api_endpoint'),
    url(r'^api/introspect$', IntrospectAPIView.as_view(), name='mikaid_introspect_api_endpoint'),
    url(r'^api/register$', RegisterAPIView.as_view(), name='mikaid_register_api_endpoint'),
    url(r'^api/users$', UserListCreateAPIView.as_view(), name='mikaid_user_list_create_api_endpoint'),
    url(r'^api/user/(?P<pk>[^/.]+)/$', UserRetrieveUpdateDestroyAPIView.as_view(), name='mikaid_user_retrieve_update_destroy_api_endpoint'),
]


# urlpatterns = format_suffix_patterns(urlpatterns)
