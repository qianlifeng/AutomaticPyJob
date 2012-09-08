#coding=gbk

from __future__ import unicode_literals
import sys,re
import urllib,urllib2,cookielib

class TBLogin():
    
    def __init__(self,user,pwd):
        #获取一个保存cookie的对象
        cj = cookielib.LWPCookieJar()
        #将一个保存cookie对象，和一个HTTP的cookie的处理器绑定
        cookie_support = urllib2.HTTPCookieProcessor(cj)
        #创建一个opener，将保存了cookie的http处理器，还有设置一个handler用于处理http的URL的打开
        opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
        #将包含了cookie、http处理器、http的handler的资源和urllib2对象板顶在一起
        urllib2.install_opener(opener)
        
        self.user,self.pwd = user,pwd
        
    def getHeaders(self):
        headers = {
        "User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.2.13) Gecko/20101203 Firefox/3.6.13",
        #"User-Agent" = "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.10 (maverick) Firefox/3.6.13",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language":"zh-cn,zh;q=0.5",
        #"Accept-Encoding":"gzip,deflate",
        "Accept-Charset":"GB2312,utf-8;q=0.7,*;q=0.7",
        "Keep-Alive":"115",
        "Connection":"keep-alive"
        }
        return headers
    
    def getLoginData(self):
        """
                    得到登陆淘宝时所需提交的数据
        """
        
        login_data = {
                'ua':'',
                'TPL_username':self.user.encode('gbk'),
                'TPL_password':self.pwd,
                'TPL_checkcode':'',
                'need_check_code':'',
                'longLogin':'1', #十天免登陆
                'action':'Authenticator',
                'event_submit_do_login':'anything',
                'TPL_redirect_url':'',
                'from':'tb',
                'fc':'default',
                'style':'default',
                'css_style':'',
                'tid':'',
                'support':'000001',
                'CtrlVersion':'1,0,0,7',
                'loginType':'3',
                'minititle':'',
                'minipara':'',
                'umto':'',
                'pstrong':'3',
#                'longLogin':'-1',
                'llnick':'',
                'sign':'',
                'need_sign':'',
                'isIgnore':'',
                'full_redirect':'',
                'popid':'',
                'callback':'',
                'guf':'',
                'not_duplite_str':'',
                'need_user_id':'',
                'poy':'',
                'gvfdcname':'',
                'gvfdcre':'',
                'from_encoding':''
                }
        return login_data
    
    def login(self):
        
        url = 'https://login.taobao.com/member/login.jhtml'        
        source = self.request(url,self.getLoginData())
        if source:
            print source
            print self.checkLoginError(source)
                 
    def checkLoginError(self,source):
        
        needVerifyCodeError = re.compile('<div id="J_Message"  class="login-msg msg">.*<p class="error">(.*?)</div>',re.S)
        r = needVerifyCodeError.search(source)
        return r.group(1) if r else None
                 
    def request(self,url,postData=dict()):
        
        postData = urllib.urlencode(postData) if postData else None
        header = self.getHeaders()
        
        req = urllib2.Request(
                url = url,
                data = postData,
                headers = header
                )
        try:
            request = urllib2.urlopen(req)
            source = request.read()
            # print request.code,request.msg
            request.close()
            return source
        except:
            info=sys.exc_info()  
            print info[0],":",info[1] 
            return None

if __name__ == '__main__':
