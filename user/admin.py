from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        ('用户信息',{'fields':['username','password','nickname','smajor','email','image']}),
        ('关注的用户',{'fields':['attention_user']}),
        ('关注的视频',{'fields':['fav_video']}),
    ]
    # 设置哪些字段可以点击进入编辑界面
    list_display = ('id','nickname','smajor','coin','exp','is_active','is_ban')

    #设置过滤器
    list_filter = ['smajor','is_active','is_ban']

    # Many to many 字段
    filter_horizontal = ('attention_user','fav_video')
admin.site.register(User,UserAdmin)
