from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse

from drones.filters import CompetitionFilter
from drones.models import DroneCategory
from drones.models import Drone
from drones.models import Pilot
from drones.models import Competition
from drones.serializers import DroneCategorySerializer
from drones.serializers import DroneSerializer
from drones.serializers import PilotSerializer
from drones.serializers import PilotCompetitionSerializer

from rest_framework.pagination import LimitOffsetPagination


class LimitOffsetPaginationWithUpperBound(LimitOffsetPagination):
    # Set the maximum limit value to 8
    max_limit = 8


from rest_framework import filters
from django_filters import AllValuesFilter, DateTimeFilter, NumberFilter


class DroneCategoryList(generics.ListCreateAPIView):
    """
    无人机类别列表
    /drone-categories/ --->> GET, POST, and OPTIONS
    """
    # pagination_class = LimitOffsetPaginationWithUpperBound

    queryset = DroneCategory.objects.all()
    serializer_class = DroneCategorySerializer
    name = 'dronecategory-list'

    filter_fields = ('name',)
    search_fields = ('^name',)
    ordering_fields = ('name', 'manufacturing_date',)


class DroneCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    无人机类别详情
    /drone-category/{id} -->> GET, PUT, PATCH, DELETE, and OPTIONS
    """
    queryset = DroneCategory.objects.all()
    serializer_class = DroneCategorySerializer
    name = 'dronecategory-detail'


class DroneList(generics.ListCreateAPIView):
    """ 无人机列表 """
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer
    name = 'drone-list'

    filter_fields = ('name', 'drone_category', 'manufacturing_date', 'has_it_competed',)


class DroneDetail(generics.RetrieveUpdateDestroyAPIView):
    """ 无人机详情 """
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer
    name = 'drone-detail'


class PilotList(generics.ListCreateAPIView):
    """ 飞行员列表 """
    queryset = Pilot.objects.all()
    serializer_class = PilotSerializer
    name = 'pilot-list'
    filter_fields = ('name', 'gender', 'races_count',)
    search_fields = ('^name',)
    ordering_fields = ('name', 'races_count')


class PilotDetail(generics.RetrieveUpdateDestroyAPIView):
    """ 飞行员详情 """
    queryset = Pilot.objects.all()
    serializer_class = PilotSerializer
    name = 'pilot-detail'


class CompetitionList(generics.ListCreateAPIView):
    """ 比赛名单列表 """
    queryset = Competition.objects.all()
    serializer_class = PilotCompetitionSerializer
    name = 'competition-list'
    filter_class =CompetitionFilter


class CompetitionDetail(generics.RetrieveUpdateDestroyAPIView):
    """ 比赛名单详情 """
    queryset = Competition.objects.all()
    serializer_class = PilotCompetitionSerializer
    name = 'competition-detail'


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'

    def get(self, request, *args, **kwargs):
        return Response({'drone-categories': reverse(DroneCategoryList.name, request=request),
                         'drones': reverse(DroneList.name, request=request),
                         'pilots': reverse(PilotList.name, request=request),
                         'competitions': reverse(CompetitionList.name, request=request)})


"""
http POST :8000/drone-categories/ name="Quadcopter"
HTTP/1.0 201 Created
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 89
Content-Type: application/json
Date: Sun, 25 Mar 2018 09:35:35 GMT
Location: http://localhost:8000/drone-categories/1
Server: WSGIServer/0.2 CPython/3.5.3
Vary: Accept, Cookie
X-Frame-Options: SAMEORIGIN

{
    "drones": [],
    "name": "Quadcopter",
    "pk": 1,
    "url": "http://localhost:8000/drone-categories/1"
}

# add 飞行员
  http POST :8000/drones/ name="WonderDrone" drone_category="Quadcopter" manufacturing_date="2017-07-20T02:02:00.716312Z" has_it_competed=false
HTTP/1.0 201 Created
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 217
Content-Type: application/json
Date: Sun, 25 Mar 2018 09:38:12 GMT
Location: http://localhost:8000/drones/1
Server: WSGIServer/0.2 CPython/3.5.3
Vary: Accept, Cookie
X-Frame-Options: SAMEORIGIN

{
    "drone_category": "Quadcopter",
    "has_it_competed": false,
    "inserted_timestamp": "2018-03-25T09:38:12.890227Z",
    "manufacturing_date": "2017-07-20T02:02:00.716312Z",
    "name": "WonderDrone",
    "url": "http://localhost:8000/drones/1"
}

http POST :8000/drones/ name="Atom" drone_category="Quadcopter" manufacturing_date="2017-08-18T02:02:00.716312Z" has_it_competed=false  


# add    pilots 
http POST :8000/pilots/ name="Penelope Pitstop" gender="F" races_count=0
HTTP/1.0 201 Created
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 194
Content-Type: application/json
Date: Sun, 25 Mar 2018 09:41:24 GMT
Location: http://localhost:8000/pilots/1
Server: WSGIServer/0.2 CPython/3.5.3
Vary: Accept, Cookie
X-Frame-Options: SAMEORIGIN

{
    "competitions": [],
    "gender": "F",
    "gender_description": "Female",
    "inserted_timestamp": "2018-03-25T09:41:24.130369Z",
    "name": "Penelope Pitstop",
    "races_count": 0,
    "url": "http://localhost:8000/pilots/1"
}

http POST :8000/pilots/ name="Peter Perfect" gender="M" races_count=0 



# add competitions比赛
http POST :8000/competitions/ distance_in_feet=800 distance_achievement_date="2017-10-20T05:03:20.776594Z" pilot="Penelope Pitstop" drone="Atom"   

http POST :8000/competitions/ distance_in_feet=2800 distance_achievement_date="2017-10-21T06:02:23.776594Z" pilot="Penelope Pitstop" drone="WonderDrone"  

http POST :8000/competitions/ distance_in_feet=790 distance_achievement_date="2017-10-20T05:43:20.776594Z" pilot="Peter Perfect" drone="Atom"  

"""

"""
http POST :8000/drone-categories/ name="Quadcopter"

http POST :8000/pilots/ name="Penelope Pitstop" gender="F"     races_count=0

HTTP/1.0 201 Created
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 194
Content-Type: application/json
Date: Sun, 25 Mar 2018 09:51:39 GMT
Location: http://localhost:8000/pilots/1
Server: WSGIServer/0.2 CPython/3.5.3
Vary: Accept, Cookie
X-Frame-Options: SAMEORIGIN

{
    "competitions": [],
    "gender": "F",
    "gender_description": "Female",
    "inserted_timestamp": "2018-03-25T09:51:39.637148Z",
    "name": "Penelope Pitstop",
    "races_count": 0,
    "url": "http://localhost:8000/pilots/1"
}

"""

"""
# 分页
curl -iX POST -H "Content-Type: application/json" -d '{"name":"Need for Speed", "drone_category":"Quadcopter", "manufacturing_date": "2017-01-20T02:02:00.716312Z", "has_it_competed": "false"}' localhost:8000/drones/  
curl -iX POST -H "Content-Type: application/json" -d '{"name":"Eclipse", "drone_category":"Octocopter", "manufacturing_date": "2017-02-20T02:02:00.716312Z", "has_it_competed": "false"}' localhost:8000/drones/   
curl -iX POST -H "Content-Type: application/json" -d '{"name":"Gossamer Albatross", "drone_category":"Quadcopter", "manufacturing_date": "2017-03-20T02:02:00.716312Z", "has_it_competed": "false"}' localhost:8000/drones/   
curl -iX POST -H "Content-Type: application/json" -d '{"name":"Dassault Falcon 7X", "drone_category":"Octocopter", "manufacturing_date": "2017-04-20T02:02:00.716312Z", "has_it_competed": "false"}' localhost:8000/drones/ 

curl -iX POST -H "Content-Type: application/json" -d '{"name":"Gulfstream I", "drone_category":"Quadcopter", "manufacturing_date": "2017-05-20T02:02:00.716312Z", "has_it_competed": "false"}' localhost:8000/drones/    

curl -iX POST -H "Content-Type: application/json" -d '{"name":"RV-3", "drone_category":"Octocopter", "manufacturing_date": "2017-06-20T02:02:00.716312Z", "has_it_competed": "false"}' localhost:8000/drones/  
curl -iX POST -H "Content-Type: application/json" -d '{"name":"Dusty", "drone_category":"Quadcopter", "manufacturing_date": "2017-07-20T02:02:00.716312Z", "has_it_competed": "false"}' localhost:8000/drones/   
curl -iX POST -H "Content-Type: application/json" -d '{"name":"Ripslinger", "drone_category":"Octocopter", "manufacturing_date": "2017-08-20T02:02:00.716312Z", "has_it_competed": "false"}' localhost:8000/drones/   
curl -iX POST -H "Content-Type: application/json" -d '{"name":"Skipper", "drone_category":"Quadcopter", "manufacturing_date": "2017-09-20T02:02:00.716312Z", "has_it_competed": "false"}' localhost:8000/drones/  
"""
