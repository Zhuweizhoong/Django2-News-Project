# -*-coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse

from django.template import RequestContext
from django.shortcuts import render_to_response
from rango.models import Category,Page
from rango.forms import CategoryForm,PageForm
from rango.forms import UserForm,UserProfileForm
from rango.forms import DIYLoginForm

from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
import datetime
from captcha.fields import CaptchaField
from django.views.decorators.csrf import csrf_protect

# Create your views here.
# def index(request):
#     return HttpResponse('Rango Rest')

def index(request):
# Request the context of the request.
# The context contains information such as the client's machine details, forexample.
#     context = RequestContext(request)
# Construct a dictionary to pass to the template engine as its context.
# Note the key boldmessage is the same as {{ boldmessage }} in the template!
    # request.session.set_test_cookie()#测试浏览器的cookies是否正常

    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {'categories': category_list, 'pages': page_list}

    visits = request.session.get('visits')
    if not visits:
        visits = 0
    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')
    if last_visit:

        last_visit_time = datetime.datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
        if (datetime.datetime.now() - last_visit_time).seconds > 0:
            # ...访问数加1...
            visits += 1
            # ...发出更新last_visit值的信号
            reset_last_visit_time = True
    else:
        print('last_visit is FALSE')
        # last_visit值不存在,发出创建last_visit值的信号.
        reset_last_visit_time = True

    context_dict['visits'] = visits
    request.session['visits'] = visits
    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.datetime.now())

    response = render(request, 'rango/index.html', context_dict)

    return response


    # for category in category_list:
    #     category.url = category.name.replace(' ','_')

# '''
# 建立cookes会话==============================================
# category_list = Category.objects.all()
#     page_list = Page.objects.order_by('-views')[:5]
#     context_dict = {'categories': category_list, 'pages': page_list}
#
#     visits = int(request.COOKIES.get('visits', '0'))
#     reset_last_view_time = False
#
#     if 'last_visit' in request.COOKIES:
#         print('last_visit in cookies')
#         last_visit  = request.COOKIES['last_visit']
#         last_visit_time  = datetime.datetime.strptime(last_visit[:-7],"%Y-%m-%d %H:%M:%S")
#
#         if (datetime.datetime.now() - last_visit_time).days> 0:
#             visits += 1
#             reset_last_view_time = True
#     else:
#         print('last_visit not in cookies')
#         reset_last_view_time = True
#         context_dict['views'] = visits
#
#     response = render(request,'rango/index.html',context_dict)
#     if reset_last_view_time:
#         print(datetime.datetime.now())
#         response.set_cookie('last_vist',datetime.datetime.now())
#     response.set_cookie('visits',visits)
#     return response
# '''====================================================================

# Return a rendered response to send to the client.
# We make use of the shortcut function to make our lives easier.
# Note that the first parameter is the template we wish to use.
    #return render_to_response('rango/index.html', context_dict,context)
    # return render(request, 'rango/index.html', context_dict)
    # return render_to_response('rango/index.html', context_dict,context)

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

#用户注册视图
def register(request):
    # if request.session.test_cookie_worked():#测试浏览器的cookies是否正常
    #     print(">>>> TEST COOKIE WORKED!")
    #     request.session.delete_test_cookie()
    # else:
    #     print('NO cookie')

    is_registered = False

    if request.method == 'POST':
        user_form = UserForm(data = request.POST)
        profile_form = UserProfileForm(data = request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()

            is_registered = True

        else:
            print(user_form.erros,profile_form.errors)
    else:
        user_form = UserForm
        profile_form = UserProfileForm

    # return render(request,
    #               'rango/register.html',
    #               {'user_form':user_form,'profile_form':profile_form,'register':is_registered})
    return render(request,
                  'rango/register.html',
                  locals())

#log in 系统
#refusence:https://www.jianshu.com/p/b403fbd8fd1f
def user_login(request):
    if request.method == 'POST':
        loginForm = DIYLoginForm(data=request.POST)
        if loginForm.is_valid():
            user_name = request.POST['username']
            pass_word = request.POST['password']

            user = authenticate(username = user_name,password = pass_word)

            if user:
                #check是否激活，可能被ban了
                if user.is_active:
                    login(request,user)
                    print('sucess!')
                    return HttpResponseRedirect('/rango/')
                else:
                    return HttpResponse('SORRY,YOU ACCOUNT IS BANNED')
            else:
                print("Invalid login details:{0},{1}".format(user_name,pass_word))
                return HttpResponse("账号或者密码错误！！！")
        else:
            return HttpResponseRedirect('/rango/login/')

    else:
        loginForm = DIYLoginForm
        context = {}
        context['loginForm'] = loginForm()
        context['user'] = request.user
        print('loginform else')
        return render(request, 'rango/login.html', context)


    # else:
    #     return render(request,
    #               'rango/login.html')


from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

# 使用login_required()装饰器来确保只有已登录的用户才可以访问这个视图
@login_required
def user_logout(request):
    # 我们只能对已登录的用户使用注销功能
    logout(request)

    # 将用户重新引导回首页.
    return HttpResponseRedirect('/rango/')

# @login_required
# def restricted(request):
#     return HttpResponse('你需要先登入啦，亲~')














