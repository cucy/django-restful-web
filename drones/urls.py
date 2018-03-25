from django.conf.urls import url
from .views import (DroneCategoryList, DroneCategoryDetail, DroneList, DroneDetail, PilotList, PilotDetail,
                    CompetitionList, CompetitionDetail, ApiRoot)

urlpatterns = [
    url(r'^drone-categories/$', DroneCategoryList.as_view(), name=DroneCategoryList.name),
    url(r'^drone-categories/(?P<pk>[0-9]+)$', DroneCategoryDetail.as_view(), name=DroneCategoryDetail.name),

    url(r'^drones/$', DroneList.as_view(), name=DroneList.name),
    url(r'^drones/(?P<pk>[0-9]+)$', DroneDetail.as_view(), name=DroneDetail.name),

    url(r'^pilots/$', PilotList.as_view(), name=PilotList.name),
    url(r'^pilots/(?P<pk>[0-9]+)$', PilotDetail.as_view(), name=PilotDetail.name),

    url(r'^competitions/$', CompetitionList.as_view(), name=CompetitionList.name),
    url(r'^competitions/(?P<pk>[0-9]+)$', CompetitionDetail.as_view(), name=CompetitionDetail.name),

    url(r'^$', ApiRoot.as_view(), name=ApiRoot.name),
]
