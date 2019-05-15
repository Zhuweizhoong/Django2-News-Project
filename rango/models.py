from django.db import models
from django.template.defaultfilters import slugify
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