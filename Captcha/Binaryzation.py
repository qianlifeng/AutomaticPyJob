#coding=gbk

from __future__ import unicode_literals
import Image
import urllib

class Binaryzation(object):
    """
    将图像进行二值化处理
    """
    
    image = None
    
    def __init__(self,img):
        self.image = img
    
    def __ConvertToGray(self):
        """
        将图片灰度化处理
        """
        if self.image:
            return self.image.convert('L')
        return None
    
    def ConvertToBinaryzation(self,b):
        """
        二值化
        b: 可以理解为亮度，大于这个亮度的全部变为纯白色
        """
        if self.image:
            self.image = self.__ConvertToGray()
            return self.image.point(lambda i:i > b and 255)
        return None


if __name__ == '__main__':
    url = 'http://regcheckcode.taobao.com/auction/checkcode?sessionID=f06c56ea0e0bda9a9d71832422b68f29'
    s = urllib.urlopen(url).read()
    f = open('v.jpg','wb')
    f.write(s)
    f.close()
    im = Image.open('v.jpg')
    b =  Binaryzation(im)
    im = b.ConvertToBinaryzation(160)
    im.show()