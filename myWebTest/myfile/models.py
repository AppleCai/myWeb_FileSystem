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
    )
    FileName_text = models.CharField(max_length=200)
    modify_date = models.DateTimeField('date published')
    FilePath_text = models.CharField(max_length=200)
    tag_text = models.CharField(max_length=200,default="",blank=True)
    status = models.IntegerField(default=0, help_text='选择类型', verbose_name='归类', choices=TYPE_CHOICES)
    def __str__(self):
        return self.FileName_text






