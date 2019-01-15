# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate
from django.db.models import Q, Prefetch
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.utils.http import urlquote
from rest_framework import exceptions, serializers
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator

from foundation.models import User


class UserListCreateSerializer(serializers.ModelSerializer):

    # Meta Information.
    class Meta:
        model = User
        fields = (
            'id',
            'avatar',
            'birthdate',
            'created_at',
            'email',
            'first_name',
            'gender',
            'groups',
            'id',
            'is_active',
            'is_ok_to_email',
            'is_ok_to_text',
            'is_staff',
            'is_superuser',
            'last_login',
            'last_modified_at',
            'last_name',
            'middle_name',
            'nationality',
            'password',
            'pr_access_code',
            'pr_expiry_date',
            'salt',
            'tenant_id',
            'type_of',
            'user_permissions',
            'was_email_activated'
        )
        extra_kwargs = {
        }

    def setup_eager_loading(cls, queryset):
        """ Perform necessary eager loading of data. """
        queryset = queryset.prefetch_related(
        )
        return queryset

    def create(self, validated_data):

        # Return our validated data.
        return validated_data


class UserRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'avatar',
            'birthdate',
            'created_at',
            'email',
            'first_name',
            'gender',
            'groups',
            'id',
            'is_active',
            'is_ok_to_email',
            'is_ok_to_text',
            'is_staff',
            'is_superuser',
            'last_login',
            'last_modified_at',
            'last_name',
            'middle_name',
            'nationality',
            'password',
            'pr_access_code',
            'pr_expiry_date',
            'salt',
            'tenant_id',
            'type_of',
            'user_permissions',
            'was_email_activated'
        )

    def validate(self, data):
        return data

    def update(self, instance, validated_data):

        # Return our validated data.
        return validated_data
