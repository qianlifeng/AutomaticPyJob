#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import unittest
from HttpWrapper import HttpWrapper,HttpWrapperException 

proxies = {'http':'10.182.46.232:80','https':'10.182.45.231:80'}

class HttpWrapperTestCase(unittest.TestCase):
    def PageNotFind(self):
        r = HttpWrapper('http://www.cnblogs.com/scottqiantest',enableProxy = True,proxyDict = proxies)
        assert r.GetResponseCode() == 404
        #print r.GetContent().decode('utf-8').encode("GB18030") #encode to GB18030 for displaying in cmd window
        #print r.GetHeaderInfo()
        #with self.assertRaises(HttpWrapperException):
            #r.GetContent()

    def CorrectRequest(self):
        r = HttpWrapper('http://www.cnblogs.com')
        assert r.GetResponseCode() == 200

    def PostDataRequest(self):
        data = {'tbUserName'        : '1',
                'tbPassword'        : '1',
                '__EVENTTARGET'     : 'btnLogin',
                '__EVENTARGUMENT'   : '',
                '__VIEWSTATE'       : '/wEPDwULLTE1MzYzODg2NzZkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYBBQtjaGtSZW1lbWJlcm1QYDyKKI9af4b67Mzq2xFaL9Bt',
                '__EVENTVALIDATION' : '/wEWBQLWwpqPDQLyj/OQAgK3jsrkBALR55GJDgKC3IeGDE1m7t2mGlasoP1Hd9hLaFoI2G05'}
        r = HttpWrapper('http://passport.cnblogs.com/login.aspx',data)
        assert r.GetContent().decode('utf-8').find(u'用户不存在') > 0
    
    def RefererRequest(self):
        #tell server I'm from baidu.com
        r = HttpWrapper('http://www.stardrifter.org/cgi-bin/ref.cgi',referer='http://www.baidu.com')
        assert r.GetResponseCode() == 200
        assert r.GetContent().find(u'www.baidu.com') > 0

    def AutoRedirectRequest(self):
        #auto redirect is enabled by default in HttpWrapper
        r = HttpWrapper('http://jigsaw.w3.org/HTTP/300/301.html',enableAutoRedirect = False)
        print r.GetResponseCode()
        assert r.GetUrl() == 'http://jigsaw.w3.org/HTTP/300/Overview.html'

        #r = HttpWrapper('http://jigsaw.w3.org/HTTP/300/302.html')
        #assert r.GetUrl() == 'http://jigsaw.w3.org/HTTP/300/Overview.html'

def suite():
    suite = unittest.TestSuite()
    suite.addTest(HttpWrapperTestCase('PageNotFind'))
    #suite.addTest(HttpWrapperTestCase('CorrectRequest'))
    #suite.addTest(HttpWrapperTestCase('PostDataRequest'))
    #suite.addTest(HttpWrapperTestCase('RefererRequest'))
    #suite.addTest(HttpWrapperTestCase('AutoRedirectRequest'))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest = 'suite')
