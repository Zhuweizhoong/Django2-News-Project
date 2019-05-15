from django.contrib import admin
from rango.models import Category, Page

class PageAdmin(admin.ModelAdmin):
    list_display = ('title' , 'category' ,'url')

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    # list_display = ('name', 'views', 'likes')

# Register your models here.
admin.site.register(Category,CategoryAdmin)
admin.site.register(Page,PageAdmin)