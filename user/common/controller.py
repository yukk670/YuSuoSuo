import re
from user.models import User
from django.shortcuts import redirect
from django.http.response import JsonResponse

redirect_field_name = 'next'
login_url = '/user/login'
AJAX_TYPE = ("ActiveXObject", "XMLHttpRequest")


def login_required(function):
    """
    需要登录后才能进行操作
    :param function: 需要登录才能执行的视图函数
    :return: 当发送过来的请求为Ajax的时候，返回包含（result,message）的JSON对象;当请求为非ajax时，跳转至/user/login
    """

    def validate(*args, **kwargs):
        request = args[0]
        if request.session.get("id"):
            return function(*args, **kwargs)
        else:
            if request.headers.get("X-Requested-With") in AJAX_TYPE:
                return JsonResponse({"result": 0, "message": "请登录后在进行该操作！"})
            else:
                return redirect(login_url, {redirect_field_name: request.path})

    return validate

def re_user_password(password):
    """
    验证用户密码
    :param password: 密码8-16的长度，必须包含字母和数字
    :return: 合格为True
    """
    return re.match(r"^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{8,16}$", password)

def re_login_register(username, password):
    """
    正则验证登陆注册的格式
    :param username:用户名长度为6-10
    :param password:密码8-16的长度，必须包含字母和数字
    :return:正确返回user对象，错误返回None
    """
    user = None
    # 用户名长度为6-10
    if not re.match(r"^[a-zA-Z0-9]{6,10}$", username):
        return user
    # 密码8-16的长度，必须包含字母和数字
    if not re_user_password(password):
        return user
    try:
        return User.objects.get(username=username)
    except:
        return user

def re_userinfo(id, nickname, email):
    """
    正则验证用户信息的格式
    :param id:user.id
    :param nickname:昵称
    :param email: 邮箱
    :return: False验证不通过,True验证通过
    """
    if not 2 <= len(nickname) <= 4:  # 用户昵称长度为2-4
        return False;
    if not re.match(r"^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$", email):  # 邮箱验证
        return False
    return True

class Favorite:

    def __init__(self, request, fav_type,att_id):
        """
        处理一切关注、收藏的操作
        :param request:
        :param fav_type:一个整数！整数含义：[0:关注用户,1:]
        """
        self.request = request
        self.att_id = att_id
        __handler_funs = (self.fav_user,)
        try:
            self.__fun = __handler_funs[fav_type]
        except IndexError:
            raise IndexError

    def do_favorite(self, is_put):
        # 1.根据不同的fav_type对不同的事物进行关注
        obj = self.__fun()

        # 是关注还是取消关注
        # if self.request.is_attenation:
        #     obj.save()
        # else:
        #     obj.delete()

    def fav_user(self):
        id = self.request.session.get("id")
        print(id)
        user = User.objects.get(id=id)
        user.attention_user.add(User.objects.get(id = 2))
        user.save()
        print(user.attention_user.all())



