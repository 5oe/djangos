from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse  # 返回json 数据
from django.conf import settings  # 导入settings ，来得到 BASE_DIR ,得到项目路径
import os  # 通过os 来拼接文件路径，创建文件夹
import uuid  # 通过uuid 生成随机码，防止上传的文件名重复
import time  # 通过时间来创建文件夹，所以需要时间


# 创建图片存放文件夹
def createfiles(path):
    file_dirs = os.path.join(settings.BASE_DIR, 'static', 'upload', path)  # 拼接文件存放地址
    path = os.path.join('static/upload/', path)  # 图片路径地址
    if not os.path.exists(file_dirs):  # 是否包含这个文件夹，如果没有就创建
        os.makedirs(file_dirs)  # 创建层级目录 2017/02/03
    return path


#  这里注意下文件存放地址 和图片地址
#  文件地址为 项目目录下的文件夹地址，它为：项目路径+图片路径
#  图片地址 只需要图片文件夹的相对路径就可以  在浏览器中为
#  http://127.0.0.1:8000/static/upload/2017/02/03/xxx.jpg


# kindedit 图片上传
@csrf_exempt
def upload_image(request):  # kindedit filename
    file = request.FILES.get('imgFile', None)  # kindedit type=file name = imgFile
    ext_name = file.name.rfind('.')  # 查找上传的 图片后缀 .png ,.jpg
    localtime = time.strftime('%Y/%m/%d', time.localtime())  # 格式化当前时间 2017/02/03
    path = createfiles(localtime) + '/'
    print(path)
    file_name = str(uuid.uuid1()) + file.name[ext_name:]  # 用uuid生成随机文件名
    file_path = os.path.join(path, file_name)  # 上传文件地址 图片路径+文件名
    print(file_path)
    with open(file_path, 'wb') as f:  # 文件写入用二进制 'wb'
        for temp in file.chunks():  # 将request获得的图片文件，写入本地
            f.write(temp)
    dic = {  # 服务器返回数据，kindedit 接受json
        'error': 0,  # error 0个错误
        'url': '/' + file_path,  # 图片路径 ，注意前面要加 '/'
        'message': '错误了...'
    }
    print(dic['url'])

    return JsonResponse(dic)
