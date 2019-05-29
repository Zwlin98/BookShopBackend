# Generated by Django 2.2.1 on 2019-05-29 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('announcement_id', models.AutoField(primary_key=True, serialize=False, verbose_name='公告编号')),
                ('announcement_content', models.TextField(blank=True, null=True, verbose_name='公告内容')),
                ('announcement_publish_time', models.DateTimeField(auto_now_add=True, verbose_name='公告发布时间')),
                ('announcement_modify_time', models.DateTimeField(auto_now=True, verbose_name='公告修改时间')),
                ('announcement_picture', models.TextField(blank=True, null=True, verbose_name='公告图片')),
            ],
            options={
                'verbose_name': '公告',
                'verbose_name_plural': '公告',
            },
        ),
    ]
