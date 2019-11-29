from django.db import models


# Create your models here.
# pip install PyMySQL
class Article(models.Model):
    title = models.CharField(max_length=255, verbose_name='标题')
    summary = models.CharField(max_length=255, verbose_name='内容')
    a_url = models.CharField(max_length=255, verbose_name='文章地址')
    img_url = models.CharField(max_length=255, verbose_name='图片地址')
    tags = models.CharField(max_length=255, verbose_name='标签')

    class Meta:
        db_table = 'article'
