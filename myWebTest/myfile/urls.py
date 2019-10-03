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
path('', views.index, name='index'),
path('update/', views.update, name='update'),
path('results/', views.results, name='results'),
]