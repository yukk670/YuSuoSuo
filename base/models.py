from django.db import models
from django.utils import timezone
from hashid_field import HashidAutoField

# 用户专业
USER_SMAJOR = ((0, "计算机科学与技术"),)
# 学历
DEGREE = ((0, "无"), (1, "本科"))
# 视频分类
VIDEO_CLASSIFY = ((0, "教育"), (1, "娱乐"))
# 语言类型
LANGUAGE_TYPE = ((0, "中文(简体)"), (1, "English"))


# 轮播图表
class Banner(models.Model):
    id = HashidAutoField(primary_key=1)
    title = models.CharField('标题', max_length=128)
    image = models.ImageField('轮播图片', upload_to='images/banner')
    url = models.CharField('链接地址', max_length=200)
    putaway_time = models.DateTimeField('发布时间', default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = '轮播图表'


# 视频表
class Video(models.Model):
    id = HashidAutoField(primary_key=1)
    name = models.CharField('视频名称', max_length=128)
    poster = models.ImageField("预览图", blank=1)
    url = models.URLField("视频链接", blank=1)
    classify = models.IntegerField("视屏分类", choices=VIDEO_CLASSIFY, default=0)
    click_count = models.IntegerField("视频点击数", default=0)
    desc = models.TextField("视频描述")
    cost_coin = models.IntegerField("消费的金币", default=0)
    putaway_time = models.DateTimeField('上架时间', default=timezone.now)

    putaway_user = models.OneToOneField('user.User', related_name='putaway_user', on_delete=models.CASCADE,
                                        verbose_name='发布者', null=1, blank=1)
    buy_user = models.ManyToManyField('user.User', related_name='v_buy_user',
                                      verbose_name='购买者', blank=1)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '视频信息'
        verbose_name_plural = '视频表'
        ordering = ['name']


# 视频字幕表
class Subtitle(models.Model):
    language = models.IntegerField('翻译语', choices=LANGUAGE_TYPE, default=0)
    subtitle = models.FileField("字幕", upload_to='course/subtitle')
    cost_coin = models.IntegerField("消费的金币", default=0)
    click_count = models.IntegerField("字幕点击数", default=0)
    video = models.ForeignKey(Video, verbose_name="视频", on_delete=models.CASCADE, null=1, blank=1)
    putaway_user = models.OneToOneField('user.User', on_delete=models.CASCADE,
                                        verbose_name='发布者', null=1, blank=1)
    buy_user = models.ManyToManyField('user.User', related_name='s_buy_user',
                                      verbose_name='购买者', blank=1)

    def __str__(self):
        if self.putaway_user:
            return f'{self.putaway_user.username}({LANGUAGE_TYPE[self.language][1]})'
        else:
            return "默认字幕"

    class Meta:
        verbose_name = '视频字幕信息'
        verbose_name_plural = '视频字幕表'

# 1.视频字幕如果没有发布者，默认为官方发布
# 2.单视频靠金币解锁   无需知道课程总值，习题金币自定义，单要给一系列课程加入总金币消费，和总习题给予的金币奖励
#   3.发布者为Null的为官方发布
