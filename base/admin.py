from django.contrib import admin
from base.models import Video,Subtitle,Banner
from course.models import CourseVideo

class CourseVideoInline(admin.TabularInline):
    model = CourseVideo
    raw_id_fields = ('video','course')
    verbose_name_plural = "课程视频绑定"
    extra = 1

class VideoAdmin(admin.ModelAdmin):
    inlines = (CourseVideoInline,)
    fieldsets = [
        ('视频信息', {'fields': ['name', 'poster', 'classify','cost_coin', 'desc','url']}),
    ]
    list_display = ('name', 'classify', 'click_count', 'putaway_time','cost_coin')
    list_filter = ['classify','click_count','putaway_time']
    search_fields = ['name',]


class SubtitleAdmin(admin.ModelAdmin):
    fieldsets = [
        ('字幕信息',{'fields':['subtitle','cost_coin','language']}),
        ('绑定视频',{'fields':['video',]}),
    ]

    list_display = ['__str__','video','cost_coin']
    list_filter = ['video',]



admin.site.register(Video,VideoAdmin)
admin.site.register(Subtitle,SubtitleAdmin)
