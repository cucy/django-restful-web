#!/usr/bin/env python
# _*_ coding:utf8 _*_ 
__date__ = '2018/3/25 19:17'
__author__ = 'zhourudong'

from rest_framework import permissions


class IsCurrentUserOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # The method is a safe method
            return True
        else:
            # The method isn't a safe method
            #  Only owners are granted permissions for unsafe methods
            return obj.owner == request.user
