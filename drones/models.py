from django.db import models


class DroneCategory(models.Model):
    name = models.CharField(max_length=250)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Drone(models.Model):
    """
    无人机
    """
    name = models.CharField(max_length=250)
    drone_category = models.ForeignKey(DroneCategory, related_name='drones', on_delete=models.CASCADE)
    manufacturing_date = models.DateTimeField(verbose_name="制造日期")
    has_it_competed = models.BooleanField(default=False)
    inserted_timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Pilot(models.Model):
    """
    驾驶员
    """
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = ((MALE, 'Male'), (FEMALE, 'Female'),)

    name = models.CharField(max_length=150, blank=False, default='')
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, default=MALE, )
    races_count = models.IntegerField(verbose_name="比赛计数")
    inserted_timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Competition(models.Model):
    """
    比赛
    """
    pilot = models.ForeignKey(Pilot, related_name='competitions', on_delete=models.CASCADE)
    drone = models.ForeignKey(Drone, on_delete=models.CASCADE)
    distance_in_feet = models.IntegerField()
    distance_achievement_date = models.DateTimeField()

    class Meta:
        # Order by distance in descending order
        ordering = ('-distance_in_feet',)
