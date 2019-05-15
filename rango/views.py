# -*-coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse

from django.template import RequestContext
from django.shortcuts import render_to_response
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm,PageForm
from django.views.decorators.csrf import csrf_protect

# Create your views here.
# def index(request):
#     return HttpResponse('Rango Rest')
def index(request):
# Request the context of the request.
# The context contains information such as the client's machine details, forexample.
    context = RequestContext(request)
# Construct a dictionary to pass to the template engine as its context.
# Note the key boldmessage is the same as {{ boldmessage }} in the template!
    #context_dict = {'boldmessage': "I am bold font from the context"}
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {'categories':category_list,'pages':page_list}

    for category in category_list:
        category.url = category.name.replace(' ','_')


# Return a rendered response to send to the client.
# We make use of the shortcut function to make our lives easier.
# Note that the first parameter is the template we wish to use.
    #return render_to_response('rango/index.html', context_dict,context)
    return render_to_response('rango/index.html', context_dict,context)

def about(request):
    context = RequestContext(request)
    context_dict_2 = {'myContext':'About Hello World!'}
    return render_to_response('rango/about.html',context_dict_2,context)


def category(request, category_name_slug):

    # 定义要传递给模板引擎的context_dict字典。
    context_dict = {}

    try:
        # 是否能匹配到给定的分类别名？
        # 如果匹配不到，.get() 方法会提交一个DoesNotExist的异常；
        # 匹配到的话，我们就用它来在Page表中检索出该分类的数据；
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name
        # 获取该分类下的所有页面；
        pages = Page.objects.filter(category=category)
        # 把获取到的数据存入context_dict；
        context_dict['pages'] = pages
        # 我们把分类名称也加入到context_dict中，这个值可用来在模板中校验分类是否存在。
        context_dict['category'] = category
    except Category.DoesNotExist:
        # 如果找不到分类，那么啥都不做;
        # 模板会显示“没有分类”的信息；
        pass

    return render(request, 'rango/category.html', context_dict)

# def category(request,category_name_url):
#     context = RequestContext(request)
#     category_name = category_name_url.replace('_', ' ')
#     context_dict = {'category_name':category_name}
#     try:
#         category = Category.objects.get(name = category_name)
#         pages = Page.objects.filter(category = category)
#
#         context_dict['pages'] = pages
#         context_dict['category'] = category
#     except:
#         pass
#
#     return render_to_response('rango/category.html',context_dict,context)


# def category(request, category_name_slug):
#     # 定义要传递给模板引擎的context_dict字典。
#     context_dict = {}
#     try:
#         # 是否能匹配到给定的分类别名？
#         # 如果匹配不到，.get() 方法会提交一个DoesNotExist的异常；
#         # 匹配到的话，我们就用它来在Page表中检索出该分类的数据；
#         category = Category.objects.get(slug=category_name_slug)
#         context_dict['category_name'] = category.name
#
#         # 获取该分类下的所有页面；
#         pages = Page.objects.filter(category=category)
#
#         # 把获取到的数据存入context_dict；
#         context_dict['pages'] = pages
#         # 我们把分类名称也加入到context_dict中，这个值可用来在模板中校验分类是否存在。
#         context_dict['category'] = category
#     except Category.DoesNotExist:
#         # 如果找不到分类，那么啥都不做;
#         # 模板会显示“没有分类”的信息；
#         pass
#
#     return render(request, 'rango/category.html', context_dict)



def add_category(request):
    context = RequestContext(request)

    if request.method =='POST':
        form =  CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit = True)
            return index(request)
        else:
            print(form.errors)
    else:
        form = CategoryForm()
    #如果用render_to_response会出现csrf的问题
    return render(request,'rango/add_category.html', {'form':form}, context)


# def add_page(request,category_name_url):
#     cat =  category_name_url.replace('_', ' ')
#
#     if request.method == 'POST':
#         form = PageForm(request.POST)
#
#         if form.is_valid():
#             page = form.save(commit = False)
#             page.category = cat
#             page.views = 0
#             page.save()
#             return category(request, category_name_url)
#         else:
#             print(form.errors)
#     else:
#         form = PageForm()
#
#     context_dir = {'form':form,'category':cat}
#     return render(request,'rango/add_page.html', context_dir)


def add_page(request, category_name_slug):
    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                # probably better to use a redirect here.
                return category(request, category_name_slug)
        else:
            print(form.errors)
    else:
        form = PageForm()

    return render(request, 'rango/add_page.html', {'form':form, 'category': cat})




