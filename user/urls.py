from django.urls import path
from . import views

#添加一个app_name以设置应用程序命名空间,用于模板的url分辨使用哪个视图
app_name = 'user'
urlpatterns = [
    path('login/',views.login,name="login"),
    path('register/',views.register,name="register"),
    path('logout/',views.logout,name="logout"),
    # url(r'^complete_userinfo/',views.complete_userinfo),
    path('<int:fav_type>/<int:att_id>/favorite/',views.favorite,name="favorite"),
    # path('finish_study/',views.finish_study),
]
