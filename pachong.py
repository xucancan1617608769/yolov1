# -*- coding:utf-8 -*-
import requests,re,urllib.request
import os
import numpy
import imghdr
from PIL import Image
cont = 3294;
#定义引擎函数模块
def getImg(url):
    global cont
    content = load_url(url)
    #数据获取完成，定义正则表达式，筛选数据
    reg = re.compile('"thumbURL":\s*"(.*?)"', re.S)
    data_list = data_filter(content,reg)
    #保存数据
    for index,data_url in enumerate(data_list):
        sava_data(data_url,"./data/phone1/" + str(cont) + ".jpg")
        cont+=1


#定义爬取数据的函数
def load_url(url):
    """
    作用：爬取指定url地址中的数据
    :param url: 指定的url地址
    :return: 所有爬取到的数据
    """
    print('开始爬取图片')
    my_headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
    }
    response = requests.get(url,headers=my_headers,verify=False)
    response.encoding = 'UTF-8'
    content = response.text
    print('数据爬取完成')
    return content

#定义筛选数据的函数
def data_filter(data,reg):
    """
    作用：进行数据按照指定描述的正则筛选
    :param data: 所有数据
    :param reg: 正则表达式
    :return: 返回筛选到的数据列表
    """
    print('---开始筛选数据')
    data_list = reg.findall(data)
    print('筛选数据完成')
    return data_list

#获取多少张的图片，需要什么图片
def getManyPages(keyword, pages):
    for i in range(30, 30 * pages + 30, 30):
        # 定义获取各种需要的参数数据
        url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&logid=9695859770224120715&ipn=rj&' \
              'ct=201326592&is=&fp=result&queryWord='+keyword+'&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1' \
              '&z=&ic=0&hd=&latest=&copyright=&word=%E6%89%8B%E6%9C%BA&s=&se=&tab=&width=&height=&face=0&istype=2&qc=' \
              '&nc=&fr=&expermode=&nojc=&pn=' + str(i)+ '&rn=30&gsm=1e&1631192619494='
        # 调用引擎对象，执行爬虫
        getImg(url)

#定义保存数据的函数
def sava_data(url_content,file_name):
    """
    作用：保存数据
    :param url_content:需要保存的数据
    :param file_name: 文件名称
    :return:
    """
    print('开始保存数据')
    try:
        urllib.request.urlretrieve(url_content, file_name)
        print('图片下载成功')
    except Exception as result:
        print('图片下载失败'+str(result))
    print('数据保存完成')

# 删除不是JPEG或者PNG格式的图片
def delete_error_image(father_path):
    # 获取父级目录的所有文件以及文件夹
    try:
        print("++++++筛选图片++++")
        image_dirs = os.listdir(father_path)
        for image_dir in image_dirs:
            image_dir = os.path.join(father_path, image_dir)
            # 如果是文件夹就继续获取文件夹中的图片
            if os.path.isdir(image_dir):
                images = os.listdir(image_dir)
                for image in images:
                    image = os.path.join(image_dir, image)
                    try:
                        # 获取图片的类型
                        image_type = imghdr.what(image)
                        # 如果图片格式不是JPEG同时也不是PNG就删除图片
                        imgType_list = {'jpg','jpeg'}
                        #if image_type is not 'jpeg' and image_type is not 'jpg':
                        if image_type not in imgType_list:
                            print(image_type)
                            os.remove(image)
                            print('已删除不是jpg和jpeg的图片：%s' % image)
                            continue
                        # 删除灰度图
                        img_ar = numpy.array(Image.open(image))
                        if len(img_ar.shape) is 2:
                            os.remove(image)
                            print('已删除灰度图：%s' % image)
                            continue
                        #判断图片尺寸大小,并删除小于448*448的图片
                        img=Image.open(image)
                        width=img.width
                        height=img.height
                        img.close()
                        if (width <448) or (height <448):
                            print(width, height)
                            os.remove(image)
                            print('已删除尺寸不符合的图片：%s' % image)
                    except:
                        pass
    except:
        pass

#定义主程序入口
if __name__ == '__main__':
    #getManyPages('通话',500);   #参数是爬取的内容和需要爬取多少页（每页30张图片）
    getManyPages("phone",500)
    delete_error_image("./data/")  #保存的路径位置
    print("=======爬取完成=======")
