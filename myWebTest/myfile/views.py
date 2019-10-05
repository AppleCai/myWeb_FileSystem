'''
@Description: In User Settings Edit
@Author: AppleCai
@Date: 2019-10-02 9:30:01
@LastEditTime: 2019-10-03 16:54:17
@LastEditors: Please set LastEditors
'''

from django.shortcuts import render
from .models import BasicInfo, ReviewInfo
from django.http import HttpResponse
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse
import os
import time
import datetime
import pandas as pd
# from datetime import datetime
import logging  # 引入logging模块

myfile_dir = r"F:\t1"  # 需要管理的文件夹
Filelist_result = []
# 将信息打印到控制台上
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')  # 设置日志级别

'''
@description: 客户端主页
@param {type} 
@return: 
'''


def index(request):
    return render(request, 'myfile/index.html', {'modify_date': timezone.now()})


'''
@description: 结果显示页
@param {type} 
@return: 
'''


# 添加此函数的目的是可以直接输入myfile/results来查看结果
def results(request):
    BasicInfo.objects.all().delete()
    q = BasicInfo.objects.order_by('modify_date', 'FileName_text')
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
            # 需要进行管理的文件名称后缀
            if ((os.path.splitext(full_path)[1] == '.txt') or
                    # (os.path.splitext(full_path)[1] == '.xls') or
                    # (os.path.splitext(full_path)[1] == '.xlsx') or
                    (os.path.splitext(full_path)[1] == '.pdf') or
                    (os.path.splitext(full_path)[1] == '.doc') or
                    # (os.path.splitext(full_path)[1] == '.md') or
                    (os.path.splitext(full_path)[1] == '.docx')):
                absPath = os.path.dirname(full_path)  # 打印出来为双斜杠，所以需要修改
                absFileName = os.path.basename(full_path)
                mtime = os.path.getmtime(full_path)
                file_modify_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))
                if absFileName == "CMakeCache.txt" or absFileName == "CMakeLists.txt" or absFileName == "readme.txt":
                    pass
                else:
                    # 格式为文件名，修改时间，Tag，文件路径
                    myfilelist.append((absFileName, file_modify_time, absPath.replace('\\', '/')))
                    # myfilelist.append(os.path.split(file_path)) #返回二元，一个为路径，一个为名称，但是没法直接替换斜杠
    return (myfilelist)


'''
 * @description: 对比2个list的差异，并且根据结果操作数据库
 * @param：lista和listb是输入数据，op为1代表新增操作，op为0代表删除操作
 * @return: 
'''


def compareDesigner(lista, listb, op):
    result = False
    if (op == 1):
        logging.debug("2. 新增的项如下：")
        sn = 0  # 序号只增不减
        if BasicInfo.objects.values('FileID').order_by('-FileID'):
            # [0]代表取出排序后的第一个，说明是最大的ID值
            sn = BasicInfo.objects.values('FileID').order_by('-FileID')[0].get('FileID')
        else:
            sn = 0
    else:
        logging.debug("1. 删除的项如下：")
    for i, myitem in enumerate(lista):
        if myitem not in listb:
            result = True
            logging.debug(' 表格行数{}:内容{}'.format(i + 2, myitem))  # i+1个标题+1个从0还是改成从1开始，所以为加2
            # [0] = absFileName
            # [1] = file_modify_time
            # [2] = absPath
            if (op == 1):  # 增加到数据库
                sn = sn + 1
                q = BasicInfo.objects.create(FileName_text=myitem[0], modify_date=myitem[1], FilePath_text=myitem[2],
                                             FileID=sn)
                # 把字符转为datatime格式
                reviewdate = datetime.datetime.strptime(myitem[1], '%Y-%m-%d %H:%M:%S') + datetime.timedelta(days=1)
                ReviewInfo.objects.create(review_date=reviewdate, phase=0, fID=q)  # q为外键关联的项

            else:  # 从数据库删除
                BasicInfo.objects.filter(FileName_text=myitem[0]).filter(modify_date=myitem[1]).delete()  # 删除指定条件的数据
        else:
            result = False
    if result == False:
        logging.debug(" 无")

    Filelist_result = BasicInfo.objects.order_by('modify_date', 'FileName_text')


# 点击post提交后，则进入此函数。通过对比数据文件信息和当前文件信息后，查看最终结果
def update(request):
    listNow = fileReader(myfile_dir)
    fileDataBase = BasicInfo.objects.all()
    listDataBase = []
    for item in fileDataBase:
        # 时间需要序列化，保持与时时读取的格式一致，方便对比
        file_modify_time = item.modify_date.strftime('%Y-%m-%d %H:%M:%S')
        listDataBase.append((item.FileName_text, file_modify_time, item.FilePath_text))
    # 开始对比2个表格
    logging.info("开始操作数据库")
    compareDesigner(listDataBase, listNow, 0)
    compareDesigner(listNow, listDataBase, 1)
    logging.info("结束操作数据库")
    # 显示结果
    q = BasicInfo.objects.order_by('-modify_date', 'FileName_text')
    return render(request, 'myfile/results.html', {'file_list': q})
    # return render(request,'myfile/index.html')

def mygenerate():
    for item in list(BasicInfo.objects.all()):
        # filter后是QuerySet类型，应该只有一个唯一的item，所以用p[0]（此为类）
        p=ReviewInfo.objects.filter(fID=item)
        #print (p[0].phase,p[0].review_date)
        yield item,p[0]

def exportDB(request):
    namelist=["文件号","文件名","文件路径","标签","修改日期","分类","完成复习阶段","下次复习日期"]
    if request.method == 'POST':
        excel_filepath = request.POST['excel_filepath']
    qlist = []
    # 创建列,yield返回一个元祖，[0]代表BaseInfo对象，[1]代表ReviewInfo对象
    for v in mygenerate():
        # 创建列
        qlist.append([v[0].FileID,v[0].FileName_text,v[0].FilePath_text,v[0].tag_text,v[0].modify_date.strftime('%Y-%m-%d %H:%M:%S'),v[0].status,v[1].phase,v[1].review_date.strftime('%Y-%m-%d %H:%M:%S')])
    dfDB = pd.DataFrame(data=qlist,columns=namelist)
    Fname = '/DB'+time.strftime("%Y%m%d%H%M%S", time.localtime())+'.xls'
    if os.path.exists(excel_filepath):
        dfDB.to_excel(excel_filepath+Fname, sheet_name="main", encoding='utf-8', index=False)
    else:
        os.makedirs(excel_filepath)
        dfDB.to_excel(excel_filepath+Fname, sheet_name="main", encoding='utf-8', index=False)
    return HttpResponse("已经导出csv到"+excel_filepath+Fname)

def reviewData(request):
    q = ReviewInfo.objects.all()
    for _, item in enumerate(q):
        if item.phase == 0:
            item.review_date = item.fID.modify_date + datetime.timedelta(days=1)
        elif item.phase == 1:
            item.review_date = item.fID.modify_date + datetime.timedelta(days=2)
        elif item.phase == 2:
            item.review_date = item.fID.modify_date + datetime.timedelta(days=4)
        elif item.phase == 3:
            item.review_date = item.fID.modify_date + datetime.timedelta(days=7)
        elif item.phase == 4:
            item.review_date = item.fID.modify_date + datetime.timedelta(days=15)
        elif item.phase == 5:
            item.review_date = item.fID.modify_date + datetime.timedelta(days=30)
        elif item.phase == 6:
            item.review_date = item.fID.modify_date + datetime.timedelta(days=90)
        else:
            item.review_date = timezone.now()
        item.save() #进行数据更新
    return HttpResponse("复习日期已经更新，去后台看最新日期吧！")
