#!/usr/bin/env python
# _*_ coding:utf8 _*_ 
__date__ = '2018/3/25 15:00'
__author__ = 'zhourudong'
from rest_framework import serializers

from toys.models import Toy


class ToySerializer(serializers.Serializer):
    """
    玩具序列化
    """
    pk = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=150)
    description = serializers.CharField(max_length=250)
    release_date = serializers.DateTimeField()
    toy_category = serializers.CharField(max_length=200)
    was_included_in_home = serializers.BooleanField(required=False)

    def create(self, validated_data):
        return Toy.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.release_date = validated_data.get('release_date', instance.release_date)
        instance.toy_category = validated_data.get('toy_category', instance.toy_category)
        instance.was_included_in_home = validated_data.get('was_included_in_home', instance.was_included_in_home)
        instance.save()
        return instance


"""
from datetime import datetime 
from django.utils import timezone 
from django.utils.six import BytesIO 
from rest_framework.renderers import JSONRenderer 
from rest_framework.parsers import JSONParser 
from toys.models import Toy 
from toys.serializers import ToySerializer 

toy_release_date = timezone.make_aware(datetime.now(), timezone.get_current_timezone()) 
toy1 = Toy(name='Snoopy talking action figure', description='Snoopy speaks five languages', release_date=toy_release_date, toy_category='Action figures', was_included_in_home=False) 
toy1.save()

toy2 = Toy(name='Hawaiian Barbie', description='Barbie loves Hawaii', release_date=toy_release_date, toy_category='Dolls', was_included_in_home=True) 
toy2.save()


# ----
serializer_for_toy1 = ToySerializer(toy1)
print(serializer_for_toy1.data)
{
    'description': 'Snoopy speaks five languages',
    'was_included_in_home': False,
    'release_date': '2018-03-25T07:13:26.480780Z',
    'name': 'Snoopy talking action figure',
    'pk': 1,
    'toy_category': 'Action figures'
}

 
serializer_for_toy2 = ToySerializer(toy2) 
print(serializer_for_toy2.data)

{
    'description': 'Barbie loves Hawaii',
    'was_included_in_home': True,
    'release_date': '2018-03-25T07:13:26.480780Z', 
    'name': 'Hawaiian Barbie',
    'pk': 2,
    'toy_category': 'Dolls'
}
   
   
# --------   序列化
json_renderer = JSONRenderer() 
toy1_rendered_into_json = json_renderer.render(serializer_for_toy1.data) 
toy2_rendered_into_json = json_renderer.render(serializer_for_toy2.data) 

print(toy1_rendered_into_json) 
b'{"pk":1,"name":"Snoopy talking action figure","description":"Snoopy speaks five languages","release_date":"2018-03-25T07:13:26.480780Z","toy_category":"Action figures","was_included_in_home":false}'

# ------- 反序列化    
parser = JSONParser()  
json_string_for_new_toy = '{"name":"Clash Royale play set","description":"6 figures from Clash Royale", "release_date":"2017-10-09T12:10:00.776594Z","toy_category":"Playset","was_included_in_home":false}' 
json_bytes_for_new_toy = bytes(json_string_for_new_toy, encoding="UTF-8")
stream_for_new_toy = BytesIO(json_bytes_for_new_toy) 
parsed_new_toy = parser.parse(stream_for_new_toy) 

print(parsed_new_toy) 
{'description': '6 figures from Clash Royale', 'release_date': '2017-10-09T12:10:00.776594Z', 'name': 'Clash Royale play set', 'toy_category': 'Playset', 'was_included_in_home': False}

"""
