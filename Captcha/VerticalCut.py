#coding=gbk

from __future__ import unicode_literals
import Image
import urllib
from Binaryzation import Binaryzation

class VerticalCut(object):
    '''
    垂直分割，适用于字符之间没有粘连的情况
    所谓垂直分割就是按列扫描，找到某列没有黑色像素点（已经二值化）的位置
    
    依赖于二值化
    '''

    img = None

    def __init__(self, img):
        self.img = img
        
    def getBorderPoint(self):
        """
        获得图像的左右边界，即在这个区间之外的都是空的图像。在这个区间之内才有图像
        """ 
        im = self.img 
        pixels = im.load()  
        w, h = im.size  
        
        left = -1
        right = -1
        breakout = False
        
        #找左边界
        for x in range(w):  
            for y in range(h):  
                if pixels[x, y] == 0:  #该列中的某个点为黑色
                    left = x
                    breakout = True
                    break
            if breakout:
                break
                
        breakout = False
        #找右边界
        for x in range(w-1,0,-1):  
            for y in range(h):  
                if pixels[x, y] == 0:  #该列中的某个点为黑色
                    right = x
                    breakout = True
                    break
            if breakout:
                break
                
        return left,right
        
    def showVerticalProjection(self,graph):  
        w = len(graph)  
        h = max(graph)  
        img = Image.new('1', (w, h))
        for x in range(w):  
            for y in range(h):  
                if y <= graph[x]:  
                    img.putpixel((x, y), 255)  
                else:  
                    break  
        img = img.transpose(Image.FLIP_TOP_BOTTOM)  
        img.show()  
    
    def cut(self):
        """
        开始垂直分割
        """
        
        if self.img:
            pixels = self.img.load()  
            w,h = self.img.size
            start,end = self.getBorderPoint()
            graph = [0] * (end - start)  #指定数组的长度
            
            #从开始到结尾，逐列扫描，把每列的像素点个数记下来
            for x in range(start, end):  
                for y in range(h):  
                    pixel = pixels[x, y]
                    if pixel == 0: # 此列有字符  
                        graph[x - start] += 1
            return graph
        
        return None
            
if __name__ == '__main__':
     
    #简单验证码地址：http://su.100steps.net/2007/vote/verify.php
    #淘宝验证码地址：http://regcheckcode.taobao.com/auction/checkcode?sessionID=f06c56ea0e0bda9a9d71832422b68f29
    url = 'http://su.100steps.net/2007/vote/verify.php'
    s = urllib.urlopen(url).read()
    f = open('v.jpg','wb')
    f.write(s)
    f.close()
    im = Image.open('v.jpg')
    b =  Binaryzation(im)
    im = b.ConvertToBinaryzation(160)
    im.show()
    v = VerticalCut(im)
    print v.cut()
        
