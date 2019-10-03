'''
@Description: In User Settings Edit
@Author: AppleCai
@Date: 2019-10-02 9:30:01
@LastEditTime: 2019-10-03 16:54:17
@LastEditors: Please set LastEditors
'''

from django.shortcuts import render
from .models import BasicInfo
from django.http import HttpResponse
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse
import os
import time
myfile_dir = r"F:\t1" #需要管理的文件夹
Filelist_result=[]

'''
@description: 客户端主页
@param {type} 
@return: 
'''
def index(request):
    if request.method == 'POST':
        excel_filename = request.POST['excel_filename']
        print(excel_filename)
    return render(request, 'myfile/index.html', {'modify_date': timezone.now()})

'''
@description: 结果显示页
@param {type} 
@return: 
'''
# 添加此函数的目的是可以直接输入myfile/results来查看结果
def results(request):
    BasicInfo.objects.all().delete()
    q = BasicInfo.objects.order_by('modify_date','FileName_text')
    return render(request, 'myfile/results.html', {'file_list': q})

'''
 * @description: 即时扫描文件夹获取目录下的文件信息
 * @param：file_dir是当前扫描的目录
 * @return: 
'''
def fileReader(file_dir):
    myfilelist = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            full_path = os.path.join(root, file)
            #需要进行管理的文件名称后缀
            if((os.path.splitext(full_path)[1]=='.txt') or
                (os.path.splitext(full_path)[1] == '.xls') or
                (os.path.splitext(full_path)[1] == '.xlsx') or
                (os.path.splitext(full_path)[1] == '.pdf')  or
                (os.path.splitext(full_path)[1] == '.doc')  or
                (os.path.splitext(full_path)[1] == '.docx') or
                (os.path.splitext(full_path)[1] == '.md')):
                absPath=os.path.dirname(full_path)       # 打印出来为双斜杠，所以需要修改
                absFileName=os.path.basename(full_path)
                mtime = os.path.getmtime(full_path)
                file_modify_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))
                #格式为文件名，修改时间，Tag，文件路径
                myfilelist.append((absFileName,file_modify_time,absPath.replace('\\','/')))
                #myfilelist.append(os.path.split(file_path)) #返回二元，一个为路径，一个为名称，但是没法直接替换斜杠
    return(myfilelist)

'''
 * @description: 对比2个list的差异，并且根据结果操作数据库
 * @param：lista和listb是输入数据，op为1代表新增操作，op为0代表删除操作
 * @return: 
'''
def compareDesigner(lista,listb,op):
    result=False
    if(op==1):
        print("1. 删除的项如下：")
    else:
        print("2. 新增的项如下：")
    for i,myitem in enumerate(lista):
        if myitem not in listb:
            result = True
            print(' 表格行数{}:内容{}'.format(i+2, myitem))  # i+1个标题+1个从0还是改成从1开始，所以为加2
            # [0] = absFileName
            # [1] = file_modify_time
            # [2] = absPath
            if(op==1):  # 增加到数据库
                BasicInfo.objects.create(FileName_text=myitem[0], modify_date=myitem[1],FilePath_text=myitem[2])
            else: # 从数据库删除
                BasicInfo.objects.filter(FileName_text=myitem[0]).filter(modify_date=myitem[1]).delete() #删除指定条件的数据
        else:
            result = False
    if  result==False:
        print(" 无")

    Filelist_result = BasicInfo.objects.order_by('modify_date','FileName_text')

# 点击post提交后，则进入此函数。通过对比数据文件信息和当前文件信息后，查看最终结果
def update(request):
    listNow=fileReader(myfile_dir)
    fileDataBase=BasicInfo.objects.all()
    listDataBase=[]
    for item in fileDataBase:
        # 时间需要序列化，保持与时时读取的格式一致，方便对比
        file_modify_time = item.modify_date.strftime('%Y-%m-%d %H:%M:%S')
        listDataBase.append((item.FileName_text,file_modify_time,item.FilePath_text))
    # 开始对比2个表格
    compareDesigner(listDataBase,listNow,0)
    compareDesigner(listNow,listDataBase,1)
    # 显示结果
    #q = BasicInfo.objects.order_by('-modify_date','FileName_text')
    return render(request, 'myfile/results.html', {'file_list': Filelist_result})
    #return render(request,'myfile/index.html')




