from django.shortcuts import render,get_object_or_404,redirect
from django.http.response import HttpResponse,JsonResponse,Http404
from .models import User
from django.contrib.auth.hashers import make_password,check_password
from django.views.decorators.http import require_POST,require_GET
from PIL import Image,ImageDraw
import random

from user.common.controller import *

"""用户登录"""
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        # 验证登陆的信息
        user = re_login_register(username,password)
        #判断用户名，密码是否匹配
        if user and check_password(password,user.password):
            request.session["nickname"] = user.nickname
            request.session["id"] = user.id
            return JsonResponse({"result":1})
        else:
            return JsonResponse({"result":0,"message":"用户名和密码不匹配！"})
    else:
        return render(request, "user/login.html")

"""用户注册"""
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = make_password(request.POST.get("password"), None, "pbkdf2_sha1")
        # 验证注册的信息
        if re_login_register(username,password):
            return JsonResponse({"result": 0, "message": "用户已存在！"})
        else:#注册用户
            try:
                user = User.objects.create(username=username,password=password,nickname=username)
            except Exception as e:
                print(e)
                return JsonResponse({"result": 0, "message": "注册失败！"})
            request.session["nickname"] = user.nickname
            request.session["id"] = user.id
            return JsonResponse({"result": 1})
    else:
        return render(request,"user/register.html")

"""用户注销"""
@login_required
def logout(request):
    try:
        del request.session["nickname"]
        del request.session["id"]
    except Exception as e:
        print(e)
    return redirect("/user/login")

"""密码重置"""
@login_required
@require_POST
def password_reset(request):
    password = request.POST.get('password')
    if re_user_password(password):
        user = User.objects.get(id = request.session["id"])
        user.password = password
        user.save()
        return JsonResponse({"result":1})
    raise Http404("您所访问的页面不存在")

"""个人信息"""
def userinfo(request):
    user = get_object_or_404(User, username=request.session["user_id"])
    if request.method == "POST":
        nickname = request.POST.get("nickname")
        email = request.POST.get("email")
        if re_userinfo(user.id,nickname,email):
            user.nickname,user.email = nickname,email
            try:
                user.save()
                return JsonResponse({"result": 1, "message": "修改成功！"})
            except Exception as e:
                print(e)
                return JsonResponse({"result": 0, "message": "修改失败！"})
    else:
        return render(request, "user/userinfo.html",user)

"""用户验证"""
def verify(request):
    #创建画布
    im = Image.new('RGB',(100,25),0x997679)
    #创建画笔
    draw = ImageDraw.Draw(im)
    for i in range(8):
        x1,y1 = random.randrange(0,100),random.randrange(0,25)
        x2,y2 = random.randrange(0,100),random.randrange(0,25)
        draw.line((x1,y1,x2,y2),[random.randrange(0,255) for i in range(3)])
    for i in range(8):
        x1,y1 = random.randrange(0,100),random.randrange(0,25)
        draw.point((x1,y1),[random.randrange(0,255) for i in range(3)])
    return HttpResponse("231234")

"""用户收藏"""
@require_GET
@login_required
def favorite(request,fav_type,att_id):
    """
    用户进行的收藏操作
    :param request:
    :param fav_type:关注类型
    :return:
    """
    """加载其他用户，主用户关注
        1.请求用户关注的所有用户,user.attention_user
        2.加载其他用户时，请求用户是否在
    """
    Favorite(request,fav_type,att_id).do_favorite(1)
    return JsonResponse({"result": 1})

"""用户已完成的学习（课程由所有章节习题集都完成决定，章节由习题集决定）"""
def finish_study(request):
    return JsonResponse(1111)