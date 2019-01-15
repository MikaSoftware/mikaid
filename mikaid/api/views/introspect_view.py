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
from oauth2_provider.contrib.rest_framework import OAuth2Authentication, TokenHasScope
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins # See: http://www.django-rest-framework.org/api-guide/generic-views/#mixins
from rest_framework import authentication, viewsets, permissions, status, parsers, renderers
from rest_framework.decorators import detail_route, list_route # See: http://www.django-rest-framework.org/api-guide/viewsets/#marking-extra-actions-for-routing
from rest_framework.response import Response


class IntrospectAPIView(APIView):
    """
    API endpoint used to provide `introspection` for the inputted token. It is
    important to note that only the owner of the oAuth 2.0 application is the
    owner of this resource.

    Notes:
    (1) https://django-oauth-toolkit.readthedocs.io/en/latest/resource_server.html
    """
    authentication_classes= (OAuth2Authentication,)
    permission_classes = (
        TokenHasScope,
    )
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.JSONParser,
    )

    renderer_classes = (renderers.JSONRenderer,)
    required_scopes = []
    throttle_classes = ()

    def post(self, request):
        # Fetch our data inputs.
        token_str = request.POST.get('token', None)
        authenticated_user = request.user
        access_token = AccessToken.objects.filter(token=token_str).first()

        # Return 404 error if access token was not found.
        if not access_token:
            return Response(data = {}, status=status.HTTP_404_NOT_FOUND)

        # If the authenticated user is not the owner of this resource.
        if authenticated_user != access_token.application.user:
            return Response(
                data = {
                    "details": "You have not been authorized to access this resource."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        # The following code will return the introspection data based on the
        # RFC. See details: https://tools.ietf.org/html/rfc7662#section-2.2
        return Response(
            data = {
                # --- REQUIRED --- #
                "active": access_token.is_valid(),

                # --- OPTIONAL --- #
                "client_id": access_token.user.id,
                "email": access_token.user.email,
                "scope": access_token.scope,
                # "exp": int(format(access_token.expires, 'U'))
                "exp": access_token.expires,
            },
            status=status.HTTP_200_OK
        )
