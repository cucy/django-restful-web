from django.db import models


class Toy(models.Model):
    """
    玩具
    """
    created = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    name = models.CharField(max_length=150, blank=False, default="")
    description = models.CharField(max_length=250, blank=True, default="", verbose_name="描述详情")
    toy_category = models.CharField(max_length=200, blank=False, default='', verbose_name="分类")
    release_date = models.DateTimeField(verbose_name="发布时间"
                                                     "")
    was_included_in_home = models.BooleanField(default=False)

    class Meta:
        ordering = ('name',)
