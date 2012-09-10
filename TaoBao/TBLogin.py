#coding=gbk

from __future__ import unicode_literals
import sys,re,os
import urllib,urllib2,cookielib

class TBLogin():
    
    user = None
    pwd = None
    
    __verifyCode = re.compile('<img id="J_StandardCode_m" .*?src="(.*?)".*?>',re.S)
    __commonError = re.compile('<div id="J_Message"  class="login-msg msg">.*<p class="error">(.*?)</div>',re.S)
    
    def __init__(self,user=None,pwd=None):
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
                #ua 据说是记录用户点击和输入信息的
                'ua':'084tRPCEzNDcxNjgzNTAyMTY9U=|tRODwiImJyLV|tSPCtSJklidWZvaHIsITU8IidZbmRvZ3NyLV1Q==|tRODwiI3liLV|tTPCtYODwgPCEyNjM8JjY0PCEyODA8KDAwPCEyODA8JzYwPV1Q==|tYPCIiLV|tZPCIiLV|tRODwiLG9iLV|tRMTwrUihkdHBzej8vLG9naW5uJHFvYmFvbiNvbW8tZW1iZWJ/LG9naW5uKmhkfWxvMnVkaWJ1Y2R1UlxNOGR0cHUjMUUiNkUiNkd3d34kcW9iYW9uI29tZSI2QiwiKGR0cHo/LyxvZ2lubiRxb2Jhb24jb21vLWVtYmVifyxvZ29ldH4qaGR9bG8zcH1tMT4hMDAwMzg2PiA+Jj4pMjM3NDk2Jm00f2B2L2V0fTRydXVmInVkaWJ1Y2R1UlxNOGR0cHUjMUUiNkUiNkd3d34kcW9iYW9uI29tZSI2Qi1dU=|tRMjwiLG9naW5iLV|tRODwiKWRiLV|tRODwiJ2xjf2ItU=|tRMDwiK1Q1MzI5PCxSITM0NTk1MjMxNTkwMjxwPiE0Mzg2NzY0NDg4MTIzNjI3PFIsIT1SLV|tRMzwrUidZbmRvZ3NyLCInWU5AITE8IzwjMDA8IjcxMi1dU=|tRODwiLWByLV|tUPCtSIiwpNDQ8IjM3PCEwNDQwPV1Q==|tRODwiLWNiLV|tVPCtSIiwrUTA2NjwiNjY9XCA8IiIsITA3NTA9XV|tRODwiJmliLV|tXPCtSIiwhPCEwNzU2PV1Q==|tRODwiLWByLV|tUPCtSIiwhMDU0PCMwMTwhMjE5Nz1dU=|tRODwiLWNiLV|tVPCtSIiwrUTA1NDwjMDE9XCA8IiIsITIzMDQ9XV|tRODwiK2NyLV|tWPCtSIiwhMjM8IDwhMzA0MD1dU=|tRODwiLWNiLV|tVPCtSIiwrUTA1NDwjMDE9XCA8IiIsITQxNDE9XV|tRODwiJmliLV|tXPCtSIiwgPCIwMjE1PV1Q==|tRODwiLWNiLV|tVPCtSKk9TUWZlbE9naW5jSGVja2IsK1g1MTwiNTI9XCA8IiIsITA2OTMwPV1Q==|tRODwiJmliLV|tXPCtSIiwhPCEwNjk0Mj1dU=|tRODwiJmliLV|tXPCtSKk9TUWZlbE9naW5jSGVja2IsITwhMDY5NTQ9XV|tRODwiLWByLV|tUPCtSKk9TUWZlbE9naW5jSGVja2IsKDUwPCI1MzwhMDc2MDY9XV|tRODwiLWNiLV|tVPCtSKk9TUWZlbE9naW5jSGVja2IsK1g1MDwiNTY9XCA8IiIsITA4MjgyPV1Q==|tRODwiLWNiLV|tVPCtSKk9TUWZlbE9naW5jSGVja2IsK1g1MDwiNTY9XCA8IiIsITA4OTEzPV1Q==|tRODwiLWNiLV|tVPCtSKk9TUWZlbE9naW5jSGVja2IsK1g1MDwiNTY9XCA8IiIsITA5NjAwPV1Q==|tRODwiLWNiLV|tVPCtSKk9TUWZlbE9naW5jSGVja2IsK1g1MDwiNTY9XCA8IiIsITEwNTU4PV1Q==|tRODwiLWNiLV|tVPCtSKk9TUWZlbE9naW5jSGVja2IsK1g1MDwiNTY9XCA8IiIsITExMjA5PV1Q==|tRODwiLWNiLV|tVPCtSKk9TUWZlbE9naW5jSGVja2IsK1g1NDwiNTE9XCA8IiIsITEyNjc0PV1Q==|tRODwiLWNiLV|tVPCtSKk9TUWZlbE9naW5jSGVja2IsK1g1MDwiNTM9XCA8IiIsITE5MTk2PV1Q==|tRODwiLWNiLV|tVPCtSKk9TUWZlbE9naW5jSGVja2IsK1g1MDwiNTM9XCA8IiIsITIwOTk2PV1Q==|tRODwiJmliLV|tXPCtSKk9TUWZlbE9naW5jSGVja2IsIDwhMjQyODQ9XV|tRODwiJmliLV|tXPCtSIiwgPCEyNDMwMD1dU=',
                'TPL_username':self.user.encode('gbk'),
                'TPL_password':self.pwd,
                'TPL_checkcode':'http://www.taobao.com',
                'need_check_code':'',
                'longLogin':'1', #十天免登陆
                'action':'Authenticator',
                'event_submit_do_login':'anything',
                'TPL_redirect_url':'',
                'from':'tb',
                'fc':'default',
                'style':'default',
                'css_style':'',
                'tid':'XOR_1_000000000000000000000000000000_6358475540797D727877707E',
                'support':'000001',
                'CtrlVersion':'1,0,0,7',
                'loginType':'3',
                'minititle':'',
                'minipara':'',
                'umto':'Te2cf41fa2b993f1082c87e7decec3f65',
                'pstrong':'2',
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
                'gvfdcname':'10',
                'gvfdcre':'', #可以没有
                'from_encoding':''
                }
        return login_data
    
    def checkLoginSucceed(self):
        s = self.request('http://i.taobao.com')
        print s
    
    def login(self,postData = None):
        
        if postData is None:
            postData = self.getLoginData() 
            
        url = 'http://login.taobao.com/member/login.jhtml?spm=1.1000386.0.2.61c0ef&f=top&redirectURL=http://trade.taobao.com/trade/itemlist/list_bought_items.htm'        
        source = self.request(url,postData)
        if source:
            error = self.checkLoginError(source)
            if error:
                print error
                if error.find('为了您的账号安全，请输入验证码。') != -1 \
                or error.find('验证码错误，请重新输入。') != -1:
                    r = self.__verifyCode.search(source)
                    if r:
                        s = self.request(r.group(1).replace('https:','http:'))
                        f = open("verifyCode.jpg","wb")
                        f.write(s)
                        f.close()
                        os.system('verifyCode.jpg')
                        postData['need_check_code'] = 'true'
                        postData['TPL_checkcode'] = raw_input("please input verifycode:")
                        self.login(postData)
                
                if error.find('您输入的密码和账户名不匹配，请重新输入') != -1:
                    print '您输入的密码和账户名不匹配，请重新输入'
                    return
            else:
#                self.checkLoginSucceed()
                print self.request('http://taojinbi.taobao.com/record/coin_get.htm?spm=a1z01.1000834.0.78.9510b9&tracelog=qzindex005')
                        
                 
    def checkLoginError(self,source):      
        r = self.__commonError.search(source)
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
#            request.close()
            return source
        except:
            info=sys.exc_info()  
            print info[0],":",info[1]
            return None

if __name__ == '__main__':
    t = TBLogin()
    t.user = 'autorunforscott@163.com'
    t.pwd = 'autorun123456'
    t.login()