# -*- coding: utf-8 -*-
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions, serializers
from rest_framework.response import Response
from foundation.models import User
# from foundation import utils


class LoginSerializer(serializers.Serializer):
    tenant_id = serializers.IntegerField(required=False)
    email = serializers.CharField(required=True, allow_blank=False)
    password = serializers.CharField(required=True, allow_blank=False)

    def validate(self, attrs):
        tenant_id = attrs.get('tenant_id', 0)
        email = attrs.get('email', None)
        password = attrs.get('password', None)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise exceptions.ValidationError(_('This E-Mail address is not registered.'))

        if not user.is_active:
            raise exceptions.ValidationError(_('Your account is suspended!'))

        authenticated_user = authenticate(username=email, password=password, tenant_id=tenant_id)

        if authenticated_user:
            attrs['authenticated_user'] = authenticated_user
            return attrs
        else:
            raise exceptions.ValidationError(_('Incorrect Pasword!'))
