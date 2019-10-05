'''
@Description: In User Settings Edit
@Author: AppleCai
@Date: 2019-10-02 9:30:01
@LastEditTime: 2019-10-03 16:55:21
@LastEditors: Please set LastEditors
'''
from django.contrib import admin
from .models import BasicInfo,ReviewInfo
default_app_config = 'myfile.apps.MyfileConfig'


class BasicInfoAdmin(admin.ModelAdmin):
    # 设置显示的列,可以用自定义的函数
    list_display = ['FileName_text','tag_text','status','FilePath_text','modify_date']
    # 搜索栏包括内容 xx 在FileName_text 或 xx 在tag_text
    search_fields = ['FileName_text','tag_text']
    # 设置默认可编辑字段，在列表里就可以编辑
    list_editable = ['tag_text','status']
    # 快速搜索列表
    list_filter = ['status','modify_date']
    # 设置每页显示多少条记录，默认是100条
    list_per_page = 50
    # 设置默认排序字段，负号表示降序排序
    ordering = ('-modify_date',)
    # 列表顶部，设置为False不在顶部显示，默认为True。
    actions_on_top=True
    # 列表底部，设置为False不在底部显示，默认为False。
    actions_on_bottom=True

class ReviewInfoAdmin(admin.ModelAdmin):
    # 设置显示的列,可以用自定义的函数
    list_display = ['filenameInfo','filepathInfo','phase','review_date']
    # 搜索栏包括内容 xx 在FileName_text 或 xx 在tag_text
    search_fields = ['FileName_text','review_date']
    # 设置默认可编辑字段，在列表里就可以编辑
    list_editable = ['phase']
    # 快速搜索列表
    list_filter = ['review_date','phase']
    # 设置每页显示多少条记录，默认是100条
    list_per_page = 50
    # 设置默认排序字段，负号表示降序排序
    ordering = ('-review_date',)
    # 列表顶部，设置为False不在顶部显示，默认为True。
    actions_on_top=True
    # 列表底部，设置为False不在底部显示，默认为False。
    actions_on_bottom=True

    def filenameInfo(self, obj):
        return obj.fID.FileName_text
    filenameInfo.verbose_name="文件名"
    def filepathInfo(self, obj):
        return obj.fID.FilePath_text
    filepathInfo.verbose_name="文件路径"

admin.site.register(BasicInfo,BasicInfoAdmin)
admin.site.register(ReviewInfo,ReviewInfoAdmin)



