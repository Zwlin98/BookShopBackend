from django.db import models


class Book(models.Model):
    name = models.CharField(max_length=128, verbose_name="书名")
    author = models.CharField(max_length=128, verbose_name="作者", null=True, blank=True)
    ISBN = models.CharField(max_length=128, verbose_name='ISBN', null=True, blank=True)
    year = models.CharField(max_length=8, verbose_name='年份', blank=True, null=True)
    pages = models.IntegerField(verbose_name='页数', blank=True, null=True)
    language = models.CharField(max_length=64, verbose_name='语言', blank=True, null=True)
    category = models.CharField(verbose_name="分类", max_length=64, blank=True, null=True)
    picture = models.TextField(verbose_name="图片", null=True, blank=True)
    description = models.TextField(verbose_name="描述", null=True, blank=True)
    download_link_pdf = models.TextField(verbose_name='PDF下载链接', null=True, blank=True)
    download_link_epub = models.TextField(verbose_name='EPUB下载链接', null=True, blank=True)
    price = models.FloatField(verbose_name="价格")
    add_time = models.DateTimeField(verbose_name="添加时间", auto_now_add=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "书籍"
        verbose_name_plural = "书籍"
