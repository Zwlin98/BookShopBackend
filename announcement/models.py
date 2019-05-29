from django.db import models


class Announcement(models.Model):
    announcement_id = models.AutoField(verbose_name="公告编号", primary_key=True)

    announcement_content = models.TextField(verbose_name="公告内容", null=True, blank=True)

    announcement_publish_time = models.DateTimeField(auto_now_add=True, verbose_name="公告发布时间")

    announcement_modify_time = models.DateTimeField(auto_now=True, verbose_name="公告修改时间")

    announcement_picture = models.TextField(verbose_name="公告图片", null=True, blank=True)

    def __str__(self):
        description = "公告编号:{}公告内容:{}".format(self.announcement_id, self.announcement_content)
        return description

    class Meta:
        verbose_name_plural = "公告"
        verbose_name = "公告"
