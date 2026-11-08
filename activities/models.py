from django.db import models


class Activity(models.Model):
    title = models.CharField(max_length=100, verbose_name="活动标题")
    description = models.TextField(blank=True, verbose_name="活动简介")
    start_time = models.DateTimeField(verbose_name="开始时间")
    location = models.CharField(max_length=200, verbose_name="活动地点")

    def __str__(self):
        return self.title
