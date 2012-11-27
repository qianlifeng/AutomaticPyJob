#coding=gbk

from __future__ import unicode_literals
from TBLogin import TBLogin
import re


class TBCoin(object):
    '''
    淘金币模块
    使用之前，请确保已经使用TBLogin.py进行登录
    '''
    
    tb = TBLogin()
        
    
    def getCurrentTBCoin(self):
        """
        获得当前登录用户的淘金币数量
        返回值：成功则返回金币数量，失败则返回None
        """
        
        r = re.compile('<strong id="J_Coin">(.*?)</strong>', re.S)
        
        url  = 'http://taojinbi.taobao.com/home/award_exchange_home.htm'
        source =  self.tb.request(url)
        s = r.search(source)
        coin = s.group(1) if s else None
        return int(coin) if coin else None
        
if __name__ == '__main__':
    t = TBLogin('autorunforscott@163.com','autorun123456')
    if t.login():
        print TBCoin().getCurrentTBCoin()