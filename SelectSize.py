import os
import numpy
import imghdr
from PIL import Image
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
    delete_error_image("./data/")  #保存的路径位置
    print("=======爬取完成=======")