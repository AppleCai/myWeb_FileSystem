'''
@Description: In User Settings Edit
@Author: AppleCai
@Date: 2019-10-02 9:30:01
@LastEditTime: 2019-10-03 16:53:53
@LastEditors: Please set LastEditors
'''
from django.db import models

class BasicInfo(models.Model):
    TYPE_CHOICES = (
        (0, ''),
        (1, 'opencv'),
        (2, 'python'),
        (3, 'c++'),
        (4, 'ROS'),
        (5, 'Linux'),
        (6, '计算机视觉'),
        (7, '机器学习'),
        (8, 'Django'),
        (9, '数学算法'),
        (10, '杂项'),
        (11, '忽略'),
    )
    FileName_text = models.CharField(max_length=200,verbose_name='文件名',default="")
    modify_date = models.DateTimeField(verbose_name='发布日期')
    FilePath_text = models.CharField(max_length=200,verbose_name='文件路径')
    tag_text = models.CharField(max_length=200,default="",blank=True,verbose_name='标签')
    status = models.IntegerField(default=0, help_text='选择类型', verbose_name='归类', choices=TYPE_CHOICES)
    FileID = models.IntegerField(default=0,verbose_name='文件号')

    def __str__(self):
        return self.FileName_text

class ReviewInfo(models.Model):
    TYPE_CHOICES = (
        (0, '未开始'),
        (1, '阶段一'),
        (2, '阶段二'),
        (3, '阶段三'),
        (4, '阶段四'),
        (5, '阶段五'),
        (6, '阶段六'),
        (7, '阶段七'),
        (8, '完成'),
    )
    fID = models.ForeignKey(BasicInfo, on_delete=models.CASCADE,related_name='reviewInfo')
    review_date = models.DateTimeField(verbose_name='复习日期',blank=True)
    phase = models.IntegerField(default=0, help_text='选择阶段', verbose_name='复习阶段', choices=TYPE_CHOICES)

    def __str__(self):
        return self.fID.FileName_text





