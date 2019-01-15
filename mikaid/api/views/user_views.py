# -*- coding: utf-8 -*-
# from django_filters.rest_framework import DjangoFilterBackend
from django.conf.urls import url, include
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import filters
from rest_framework import generics
from rest_framework import authentication, viewsets, permissions, status
from rest_framework.response import Response

from api.serializers import (
    UserListCreateSerializer,
    UserRetrieveUpdateDestroySerializer
)
from api.permissions import (
   CanListCreateUserPermission,
   CanRetrieveUpdateDestroyUserPermission
)
from foundation.models import User


class UserListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = UserListCreateSerializer
    # pagination_class = StandardResultsSetPagination
    permission_classes = (
        # permissions.IsAuthenticated,
        # IsAuthenticatedAndIsActivePermission,
        # CanListCreateUserPermission
    )
    # filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    # search_fields = ('@given_name', '@middle_name', '@last_name', '@email', 'telephone',)

    def get_queryset(self):
        """
        List
        """
        # Fetch all the queries.
        queryset = User.objects.all().order_by('-email')

        # # The following code will use the 'django-filter'
        # filter = CustomerFilter(self.request.GET, queryset=queryset)
        # queryset = filter.qs

        # Return our filtered list.
        return queryset

    def post(self, request, format=None):
        """
        Create
        """
        serializer = UserListCreateSerializer(data=request.data, context={
            'created_by': request.user,
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserRetrieveUpdateDestroySerializer
    # pagination_class = StandardResultsSetPagination
    permission_classes = (
        # permissions.IsAuthenticated,
        # IsAuthenticatedAndIsActivePermission,
        # CanRetrieveUpdateDestroyUserPermission
    )

    def get(self, request, pk=None):
        """
        Retrieve
        """
        user = User.objects.filter(id=pk).first()
        if user is None:
            return Response(data=None,status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, user)  # Validate permissions.
        serializer = UserRetrieveUpdateDestroySerializer(user, many=False)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    def put(self, request, pk=None):
        """
        Update
        """
        user = User.objects.filter(id=pk).first()
        if user is None:
            return Response(data=None,status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, user)  # Validate permissions.
        serializer = UserRetrieveUpdateDestroySerializer(user, data=request.data, context={
            'last_modified_by': request.user,
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk=None):
        """
        Delete
        """
        user = User.objects.filter(id=pk).first()
        if user is None:
            return Response(data=None,status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, user)  # Validate permissions.
        user.delete()
        return Response(data=[], status=status.HTTP_200_OK)
