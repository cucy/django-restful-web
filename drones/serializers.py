from rest_framework import serializers
from drones.models import DroneCategory
from drones.models import Drone
from drones.models import Pilot
from drones.models import Competition
import drones.views


class DroneCategorySerializer(serializers.HyperlinkedModelSerializer):
    """
    无人机类型serializer
    """
    drones = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='drone-detail')

    class Meta:
        model = DroneCategory
        fields = ('url', 'pk', 'name', 'drones')


class DroneSerializer(serializers.HyperlinkedModelSerializer):
    """
    无人机 serializer
    """
    # Display the category name
    drone_category = serializers.SlugRelatedField(queryset=DroneCategory.objects.all(), slug_field='name')

    class Meta:
        model = Drone
        fields = ('url', 'name', 'drone_category', 'manufacturing_date', 'has_it_competed', 'inserted_timestamp')


class CompetitionSerializer(serializers.HyperlinkedModelSerializer):
    """
    比赛serializer
    """
    # Display all the details for the related drone
    # 显示相关的无人驾驶飞机的所有细节
    drone = DroneSerializer()

    class Meta:
        model = Competition
        fields = ('url', 'pk', 'distance_in_feet', 'distance_achievement_date', 'drone')


class PilotSerializer(serializers.HyperlinkedModelSerializer):
    """
    飞行员Serializer
    """
    competitions = CompetitionSerializer(many=True, read_only=True)  # 比赛
    gender = serializers.ChoiceField(choices=Pilot.GENDER_CHOICES)  # 性别
    gender_description = serializers.CharField(source='get_gender_display', read_only=True)

    class Meta:
        model = Pilot
        fields = ('url', 'name', 'gender', 'gender_description', 'races_count', 'inserted_timestamp', 'competitions')


class PilotCompetitionSerializer(serializers.ModelSerializer):
    """
    飞行比赛serializer
    """
    # Display the pilot's name  显示飞行员的名字
    pilot = serializers.SlugRelatedField(queryset=Pilot.objects.all(), slug_field='name')
    # Display the drone's name  显示无人驾驶飞机的名字
    drone = serializers.SlugRelatedField(queryset=Drone.objects.all(), slug_field='name')

    class Meta:
        model = Competition
        fields = ('url', 'pk', 'distance_in_feet', 'distance_achievement_date', 'pilot', 'drone')
