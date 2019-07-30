from django.contrib import admin
from .models import Course,Tree,ProblemSet
from base.admin import CourseVideoInline

class CourseAdmin(admin.ModelAdmin):
    fieldsets = [
        ('课程信息', {'fields': ['name','detail','poster','degree','per']}),
        ('前置课程', {'fields': ['require_course',]}),
        ('天赋树',{'fields':['tree']})
    ]
    list_display = ('name', 'degree', 'per','click_count')
    list_filter = ['click_count', 'degree', 'putaway_time', 'per']

    raw_id_fields = ('require_course','tree')
    inlines = [CourseVideoInline,]

class TreeAdmin(admin.ModelAdmin):
    fieldsets = [
        ('课程树',{'fields':['name','describe']}),
    ]
    list_display = ('name',)

class ProblemSetAdmin(admin.ModelAdmin):
    fieldsets = [
        ('习题信息',{'fields':['describe','answer']}),
        ('绑定视频',{'fields':['course']}),
    ]
    list_display = ('name',)
    raw_id_fields = ('course',)
    def name(self,obj):
        return obj.describe.split("#")[0]

    name.short_description = '问题名'

admin.site.register(Tree,TreeAdmin)
admin.site.register(Course,CourseAdmin)
admin.site.register(ProblemSet,ProblemSetAdmin)
