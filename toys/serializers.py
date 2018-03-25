#!/usr/bin/env python
# _*_ coding:utf8 _*_ 
__date__ = '2018/3/25 15:00'
__author__ = 'zhourudong'
from rest_framework import serializers

from toys.models import Toy


class ToySerializer(serializers.ModelSerializer):
    """
    玩具序列化
    """

    class Meta:
        model = Toy
        fields = ('id',
                  'name',
                  'description',
                  'release_date',
                  'toy_category',
                  'was_included_in_home')
