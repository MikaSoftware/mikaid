# -*- coding: utf-8 -*-
import logging
from datetime import datetime
from django.conf import settings
from django.conf.urls import url, include
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from django.db import connection # Used for django tenants.
from django.http import Http404
from django.utils import timezone
from oauthlib.common import generate_token
from oauth2_provider.models import Application, AbstractApplication, AbstractAccessToken, AccessToken, RefreshToken
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins # See: http://www.django-rest-framework.org/api-guide/generic-views/#mixins
from rest_framework import authentication, viewsets, permissions, status, parsers, renderers
from rest_framework.decorators import detail_route, list_route # See: http://www.django-rest-framework.org/api-guide/viewsets/#marking-extra-actions-for-routing
from rest_framework.response import Response

from api.serializers import RegisterSerializer


class RegisterAPIView(APIView):
    """
    API endpoint used for users to input their email and password to get the
    oAuth 2.0 token which can be used in remote resource servers.
    """
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.JSONParser,
    )

    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request):
        # Save our code and return the serialized data.
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()

        # Get the newly created user from the registration.
        authenticated_user = data['user']

        # Get our web application authorization.
        application = Application.objects.filter(name=settings.MIKAID_RESOURCE_SERVER_NAME).first()

        # Generate our access token which does not have a time limit.
        aware_dt = timezone.now()
        expires_dt = aware_dt.replace(aware_dt.year + 1776)
        access_token, created = AccessToken.objects.update_or_create(
            application=application,
            user=authenticated_user,
            defaults={
                'user': authenticated_user,
                'application': application,
                'expires': expires_dt,
                'token': generate_token(),
                'scope': 'read,write,introspection'
            },
            scope='read,write,introspection'
        )

        # Return our new token.
        return Response(
            data = {
                # --- REQUIRED --- #
                'token': str(access_token),
                'scope': access_token.scope,

                # --- OPTIONAL --- #
                "client_id": access_token.user.id,
                "email": access_token.user.email,
                # "exp": int(format(access_token.expires, 'U'))
                "exp": access_token.expires,
            },
            status=status.HTTP_201_CREATED
        )
