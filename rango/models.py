from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User#django自带的用户模型
from django.conf import settings

# Create your models here.
# class Publisher(models.Model):
#     #id = models.AutoField(primary_key=True)  # 这行代码可以省略
#     name = models.CharField(max_length=32)
#
#     def __str__(self):
#         return self.name


# class Book(models.Model):
#     name = models.CharField(max_length=32)
#     publisher = models.ForeignKey(Publisher)
#
#     def __str__(self):
#         return self.name
#
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)
    #
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Page(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)#2.0后需要加on_delete,保证唯一
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    # def __unicode__(self):
    def __str__(self):
        return self.title

class UserProfile(models.Model):
    #在django2.0后，定义外键和一对一关系的时候需要加on_delete选项，
    # 此参数为了避免两个表里的数据不一致问题，不然会报错：
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    website = models.URLField(blank=True)

    #BUG!
    #如果不重写upload函数会存在一个bug在admin和存储图像的路径上
    def upload_to(instance, fielname):
        return '/'.join([settings.MEDIA_ROOT,fielname])

    picture  = models.ImageField(upload_to='profile_images/', blank=True)
    #记得更新数据库python manage.py makemigrations + python manage.py migrate

    def __str__(self):
        return self.user.username



