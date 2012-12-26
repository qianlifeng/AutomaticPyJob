#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib,sys
import urllib2
import cookielib
import json
from mail import Mail

#作用：快盘自动签到程序
class Login_kp:
    def __init__(self):
        cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(self.opener)
        self.opener.addheaders = [('User-agent', 'IE')]

    def login(self, username, password):
        #首先访问主页，获取必要的cookie
        req1 = urllib2.Request('https://www.kuaipan.cn')
        try:
            self.opener.open(req1)
        except Exception:
            print(u'预加载失败：网络连接错误！')
            return False
        
        #try to login
        loginUrl = 'https://www.kuaipan.cn/index.php?ac=account&op=login'
        data = urllib.urlencode({'username':username, 'userpwd':password,'isajax':'yes'})
        req = urllib2.Request(loginUrl, data)
        try:
            response = self.opener.open(req)
            resHtml = response.read()
            resJson = json.loads(resHtml)
            if resJson['state'] == '0':
                if resJson['errcode'] == 'checkemailcode_2':
                    print u'email is not exist'
                    return False
                elif resJson['errcode'] == 'account_api_login_accountNotMatch':
                    print u'account not match'
                    return False
                else:
                    print u'login failed. errcode:',resJson['errcode']
                    return False

        except Exception:
            s=sys.exc_info()
            print "Error '%s' happened on line %d" % (s[1],s[2].tb_lineno)
            return False

        print(u'%s login succeed...' % username),
        return True

    def logout(self):
        url = 'http://www.kuaipan.cn/index.php?ac=account&op=logout'
        req = urllib2.Request(url)
        fd = self.opener.open(req)
        fd.close()
        
    def sign(self):
        url = 'http://www.kuaipan.cn/index.php?ac=common&op=usersign'
        req = urllib2.Request(url)
        fd = self.opener.open(req)
        signReturnJson = fd.read()
        sign_js = json.loads(signReturnJson)
        if sign_js['state'] == -102:
            print(u"has signed today!")
            Mail().SendMail(u'快盘签到',["qianlf2008@163.com"], u"今日已经在其他地方签到", "fyi.")
        elif sign_js['state'] == 1:
            o = u"签到成功! 获得积分：%d，总积分：%d；获得空间：%dM\n" % (sign_js['increase'], sign_js['status']['points'], sign_js['rewardsize'])
            print o
            Mail().SendMail(u'快盘签到',["qianlf2008@163.com"], u"签到成功", o)
        else:
            print(u"sign failed!")
        fd.close()

if __name__ == '__main__':
    l = Login_kp()
    if l.login('email', 'pwd') == False:
        exit(1)
    l.sign()
