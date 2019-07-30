# -*-coding:utf-8-*-
from django.db import models
from django.utils import timezone

from base.models import USER_SMAJOR,Video
# 用户验证方式
USER_VERIFY_TYPE = ((0, "邮箱验证"), (1, "手机验证"))
# 用户收藏类型
USER_FAVORITE_TYPE = ((0, "课程"), (1, "章节"),(2,"用户"))
# 学习的类型
STUDY_TYPE = ((0, "课程"), (1, "章节"))
# 用户反馈类型
USER_HANDLER_TYPE = ((0, "天赋树反馈"), (1, "视屏反馈"), (2, "字幕反馈"), (3, "回答反馈"))

# 用户表
class User(models.Model):
    username = models.CharField('用户名', max_length=30, db_index=1, unique=1)
    password = models.CharField("密码", max_length=128)
    nickname = models.CharField('昵称', max_length=30, null=1)
    smajor = models.IntegerField("专业", choices=USER_SMAJOR, default=0)
    coin = models.IntegerField("梭梭币", default=50)
    exp = models.IntegerField('总经验值', default=0)
    email = models.EmailField('邮箱地址', max_length=64, unique=1, null=1,blank=1)
    image = models.ImageField(upload_to='image/%Y/%m', default='image/default.png', max_length=128)
    # mobile = models.CharField('手机号',max_length=22, null=1,unique=1)
    # birthday = models.DateField(verbose_name='生日', null=True, blank=True)
    # gender = models.IntegerField('性别',choices=((0, '男'), (1, '女')), default=0)
    # address = models.CharField('地址',max_length=128, null=1, blank=1)

    # 第三方应用帐号登录

    is_active = models.BooleanField("是否激活", default=False)
    is_ban = models.BooleanField("是否禁用", default=False)

    #如果你不想在多对多关系中对称self，设置symmetrical为False
    attention_user = models.ManyToManyField('self',symmetrical=0,related_name="attention",blank=1)
    fav_video = models.ManyToManyField(Video, verbose_name="关注视频",blank=1, symmetrical=0)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = '用户表'

    def __str__(self):
        return self.nickname

# 用户收藏
class Favorite(models.Model):
    type = models.IntegerField("收藏类型", choices=USER_HANDLER_TYPE, default=0)
    type_id = models.IntegerField("收藏的类型id")

# """
# 用户已完成的学习（课程由所有章节习题集都完成决定，章节由习题集决定）
# """
# class Finsh(models.Model):
#     # 一个用户可以完成多项学习
#     user = models.ForeignKey(User,verbose_name='用户',on_delete=models.CASCADE)
#     type = models.IntegerField('学习类型',choices=STUDY_TYPE,default=0)
#     type_id = models.IntegerField('学习类型id',default=0)
#     putaway_time = models.DateTimeField('完成时间',default=timezone.now)

# 用户反馈表-- 一个用户对一个问题回答只能反馈一次
# class Feedback(models.Model):
#     type = models.IntegerField("反馈类型", choices=USER_HANDLER_TYPE, default=0)
#     type_id = models.IntegerField("反馈类型的id")
#     # 0差评、1好评
#     feedback = models.BooleanField(verbose_name="反馈结果")
#     user = models.ForeignKey(User, verbose_name="反馈的用户", on_delete=models.CASCADE,blank=1)


# """用户验证记录表"""
# class VerifyRecord(models.Model):
#     code = models.CharField(max_length=24, verbose_name='验证码')
#     send_time = models.DateTimeField(default=datetime.now, verbose_name='发送时间')
#
#     class Meta:
#         verbose_name = '验证码发送'
#         verbose_name_plural = verbose_name


# """评论表"""
# class UserComment(models.Model):
#     | uid(回答的用户id int)        |      |              |
# | comm_describe(问题描述 text) |      |              |
#     comme_id = models.IntegerField(default=0, verbose_name='收藏的类型id')
#     comment_type = models.IntegerField(choices=USER_FAVORITE_TYPE, verbose_name='评论类型')
#
# """用户消息"""
# class UserMessage(models.Model):
#     user = models.IntegerField(default=0, verbose_name='接收用户')
#     message = models.CharField(max_length=256, verbose_name='消息')
#     has_read = models.BooleanField(default=False, verbose_name='是否已读')
#     putaway_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
#
#     class Meta:
#         verbose_name = '用户消息'
#         verbose_name_plural = verbose_name
