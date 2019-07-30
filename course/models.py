# -*-coding:utf-8-*-
from django.db import models
from hashid_field import HashidAutoField

from user.models import User
from base.models import Video, DEGREE
from django.utils import timezone

# 问题选项
ANSWER_CHOICES = ((0, "A"), (1, "B"), (2, "C"), (3, "D"))

"""课程天赋树表(用于表达一系列课程)"""


class Tree(models.Model):
    name = models.CharField("课程树名称", max_length=100)

    describe = models.TextField("课程树描述")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '课程天赋'
        verbose_name_plural = '课程天赋表'


def get_uploadto(instance, filename):
    return f'course/{timezone.now():%H%M%S}{filename}'


"""课程表
1.如果课程内所有视频练习都完成视为通过课程；并追加视频提供的金币；删除对应的用户习题记录
"""


class Course(models.Model):
    id = HashidAutoField(primary_key=1)
    name = models.CharField('课程名称', max_length=128, db_index=1)
    detail = models.TextField('课程详情')
    degree = models.IntegerField('参考学历', choices=DEGREE, default=0)
    click_count = models.IntegerField('点击数', default=0)
    per = models.FloatField("完成的金币反馈率")
    putaway_time = models.DateTimeField('上架时间', default=timezone.now)
    poster = models.ImageField('预览图', upload_to=get_uploadto, blank=1)

    user = models.ManyToManyField(User, verbose_name='完成课程的用户', blank=1)
    tree = models.ForeignKey(Tree, verbose_name="课程天赋树表", on_delete=models.CASCADE, blank=1, null=1)
    require_course = models.ForeignKey('self', verbose_name="前置课程", on_delete=models.CASCADE, blank=1, null=1)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '课程信息'
        verbose_name_plural = '课程表'
        ordering = ['name']

# 课程视频表
class CourseVideo(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    index = models.IntegerField('视频顺序')

    def __str__(self):
        return self.video.name

    class Meta:
        ordering = ['index']

"""习题集
问题回答错误，扣除用户金币
"""


class ProblemSet(models.Model):
    describe = models.TextField("问题描述")
    answer = models.IntegerField("问题答案", choices=ANSWER_CHOICES)

    # 增加习题对课程的多对一引用
    course = models.ForeignKey(Course, verbose_name="哪个课程的习题", on_delete=models.CASCADE, null=1, blank=1)
    user = models.ManyToManyField('user.User', verbose_name="完成习题的用户", blank=1, symmetrical=0)

    class Meta:
        verbose_name = '习题集'
        verbose_name_plural = '习题表'

# """
# 针对章节提出的问题(提问者肯定默认关注了该问题)
# """
# class LessonQuestion(models.Model):
#     question_id = models.AutoField(primary_key=1, auto_created=1,verbose_name="问题id")
#     #一个章节可以有多个问题
#     lesson = models.ForeignKey(Lesson,verbose_name="章节")
#     user = models.OneToOneField(User,verbose_name="提问的用户")
#     title = models.CharField(max_length=80,db_index=1)
#     describe = models.TextField(verbose_name="问题描述")
#     # | ques_file（附件 ）【续】 | | |
#     # | ques_tag(问题标签)【续】 | | |
#     gold = models.IntegerField(default=0,verbose_name="悬赏值")
#     # has_remind = models.BooleanField(default=0,verbose_name="是否设定了提示!")
#
#     class Meta:
#         verbose_name = '章节问题'
#         verbose_name_plural = verbose_name
#
#
# """针对章节问题回复的答案"""
# class LessonAnswer(models.Model):
#     answer_id = models.AutoField(primary_key=1, auto_created=1,verbose_name="回答id")
#     #一个问题可以有多个回答
#     lesson_question = models.ForeignKey(LessonQuestion,verbose_name="章节问题")
#     # 每个用户对每个问题只能回答一次
#     user = models.OneToOneField(User,verbose_name="回答者")
#     message = models.CharField(max_length=256, verbose_name='回答信息')
#     answer_time = models.DateTimeField(default=datetime.now, verbose_name='回答时间')
#
#     class Meta:
#         verbose_name = '问题答复'
#         verbose_name_plural = verbose_name
