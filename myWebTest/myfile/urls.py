'''
@Description: In User Settings Edit
@Author: AppleCai
@Date: 2019-10-02 9:30:01
@LastEditTime: 2019-10-03 16:54:08
@LastEditors: Please set LastEditors
'''
from django.urls import path
from . import views
app_name = 'myfile'
urlpatterns = [
    # name是传递到html里面的，里面有url update就是来源name的值。
path('', views.index, name='index'),
path('update/', views.update, name='update'),
path('exportDB/', views.exportDB, name='exportDB'),
path('reviewData/', views.reviewData, name='reviewData'), #没有为它配置前端显示，只是设置了后台
path('results/', views.results, name='results'),
]