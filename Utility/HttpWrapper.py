#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import urllib,urllib2,cookielib,zlib
from gzip import GzipFile
from StringIO import StringIO
import sys

class HttpWrapperException(Exception):
    """
    Custom HttpWrapper Exception
    """
    pass

class HttpWrapper:
  """
  A wrapper of http Request, integrated with cookie handler and smart referer handler

  Usage:
      HttpWrapper('http://xxx.com',data=dict)
  """

  def __init__(self, url, postData=None,enableAutoRedirect = True,enableProxy = False,proxyDict = None,**header):
    """
    url                : url you want to request
    postData           : data you want to post to the server, must be dict type,like {data1 : 'data'}
    enableAutoRedirect : auto redirect when server return 301,302 error
    enableProxy        : whether enable proxy
    ProxyDict          : proxy info. e.g  ProxyDict = {'http':'10.182.45.231:80','https':'10.182.45.231:80'}
    **header           : other request info. e.g. referer='www.sina.com.cn'
    """

    self.url = url
    self.postData =  postData
    self.enableAutoRedirect = enableAutoRedirect
    self.enableProxy = enableProxy
    self.ProxyDict = proxyDict
    #tell server where i'm from,some explain about referer http://www.fwolf.com/blog/post/320
    if 'referer' in header:
        self.referer = header['referer']
    else:
        self.referer = None

    if 'user-agent' in header:
        self.user_agent = header['user-agent']
    else:
        self.user_agent = 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16'

    self.__SetupHandler()
    self.__SendRequest(self.__SetupRequest())
    
  class ContentEncodingProcessor(urllib2.BaseHandler):
    """
    A handler to add gzip capabilities to urllib2 requests 
    """
     
    # add headers to requests
    def http_request(self, req):
        req.add_header("Accept-Encoding", "gzip,deflate")
        return req
     
    # decode
    def http_response(self, req, resp):
        old_resp = resp
        # gzip
        if resp.headers.get("content-encoding") == "gzip":
            gz = GzipFile( fileobj = StringIO(resp.read()), mode="r")
            resp = urllib2.addinfourl(gz, old_resp.headers, old_resp.url, old_resp.code)
            resp.msg = old_resp.msg
        # deflate
        if resp.headers.get("content-encoding") == "deflate":
            gz = StringIO(self.deflate(resp.read()) )
            resp = urllib2.addinfourl(gz, old_resp.headers, old_resp.url, old_resp.code)  # 'class to add info() and
            resp.msg = old_resp.msg
        return resp
    
    def deflate(self,data):   # zlib only provides the zlib compress format, not the deflate format;
      try:               # so on top of all there's this workaround:
        return zlib.decompress(data, -zlib.MAX_WBITS)
      except zlib.error:
        return zlib.decompress(data)
    

  def __SetupHandler(self):
    """
    setup cookie handler, proxy handler and redirect hander for urllib2 library 
    """
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    opener.addheaders = [('User-agent', self.user_agent)]
    if self.enableAutoRedirect == True:
        opener.add_handler(urllib2.HTTPRedirectHandler())
    if self.enableProxy == True:
        if self.proxyDict == None:
            raise HttpWrapperException('you must specify proxyDict when enabled Proxy')
        opener.add_handler(urllib2.ProxyHandler(self.proxyDict))
    urllib2.install_opener(opener)
 
  def __SetupRequest(self):
    """
    setup request information
    """
    if self.url is None or self.url == '':
        raise HttpWrapperException("url can't be empty!")

    if self.postData is not None:
        req = urllib2.Request(self.url, urllib.urlencode(self.postData))
    else:
        req = urllib2.Request(self.url)

    if self.referer:
        req.add_header('referer', self.referer)

    if self.user_agent:
        req.add_header('user-agent', self.user_agent)

    return req

  def __SendRequest(self,req):
    try:
      res = urllib2.urlopen(req)
      self.source = res.read()
      self.code = res.getcode()
      #get real url, if we have 301 redirect page
      self.url = res.geturl() 
      self.head_dict = res.info().dict
      res.close()
    except urllib2.HTTPError,e:
        self.code = e.code
        self.source = e.fp.read()
        self.head_dict = e.headers
        #print e.code
        #print e.msg
        #print e.headers
        #print e.fp.read()
        #print u"error happended:\r\n Location: HttpWrapper.__SendRequest \r\n Error Information:",  sys.exc_info()[1]


  def GetResponseCode(self):
    """
    get response code, e.g. 200 or 302
    """
    if self.code:
        return self.code
    return -1

  def GetUrl(self):
    if self.url:
        return self.url
    return None

  def GetContent(self):
    """
    get content body of the response.
    usually, you need to decode those content. for example, GetContent().decode('utf-8')
    """
    if "source" in dir(self):
        return self.source
    else:
        raise HttpWrapperException(u'HttpWrapper error happended:\r\n Location: HttpWrapper.GetContent \r\n Error Information:no content find')

  def GetHeaderInfo(self):
    return self.head_dict

  def GetCookie(self):
    if 'set-cookie' in self.head_dict:
      return self.head_dict['set-cookie']
    else:
      return None

  def GetContentType(self):
    if 'content-type' in self.head_dict:
      return self.head_dict['content-type']
    else:
      return None

  def GetCharset(self):
    contentType = self.GetContentType()
    if contentType is not None:
        index = contentType.find("charset")
        if  index > 0:
           return contentType[index+8:]
    return None

  def GetExpiresTime(self):
    if 'expires' in self.head_dict:
      return self.head_dict['expires']
    else:
      return None

  def GetServerName(self):
    if 'server' in self.head_dict:
      return self.head_dict['server']
    else:
      return None

if __name__ == '__main__':
    b = HttpWrapper('http://www.sina.com/test/fe')
    print b.GetContent().decode('utf-8')
