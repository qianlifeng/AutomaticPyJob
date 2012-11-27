# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
import os,sys,subprocess,stat
import xml.dom.minidom
import codecs
from colorama import Fore, Back, Style,init

#init colorama
init()

def GreenPrint(s):
    print Fore.GREEN + s + Fore.RESET

def RedPrint(s):
    print Fore.RED + s+ Fore.RESET

def MagentaPrint(s):
    print Fore.MAGENTA + s+ Fore.RESET

def YellowPrint(s):
    print Fore.YELLOW + s+ Fore.RESET

class Prodika(object):
    '''Prodika工具箱'''

    #规范：变量小写开头，方法大写开头
    #方法前面的A_前缀是为了方法自省排序的时候使用

    prodikaPath = r'd:\WorkProject\private\lqian\v6.1.1.0_20120724\Prodika'
    

    def _ChangeCoreAppSettingValue(self,v):
        '''更改控制显示控件路径的文件节点'''
        coreAppConfig = os.path.join(self.prodikaPath,r'config\Core\CoreAppSettings.config')
        #更改文件只读属性
        os.chmod(coreAppConfig,stat.S_IWRITE)

        fileObj = open(coreAppConfig)
        x = fileObj.read()
        fileObj.close()

        doc = xml.dom.minidom.parseString(x)
        for node in doc.getElementsByTagName("config"):
            if node.parentNode.tagName == 'TranslationManager' and node.getAttribute('key') == 'CACHE_DATA_LOADER_FACTORY':
                node.setAttribute('value',v)

        fileObj = codecs.open(coreAppConfig,'w','utf-8')
        fileObj.write( doc.toxml().replace('<?xml version="1.0" ?>',''))
        fileObj.close()
        GreenPrint('文件写入成功，正在重启IIS...')
        os.system('iisreset')
        GreenPrint('Done!')

    def A_EnableControlDetailPath(self):
        '''显示控件详细路径'''

        v = 'Class:Xeno.Prodika.Translation.Loaders.PhantomTranslationCacheDataLoaderFactory,PlatformExtensions'
        self._ChangeCoreAppSettingValue(v)

    def A_UnEnableControlDetailPath(self):
        '''不显示控件详细路径'''

        v = 'Class:Xeno.Prodika.Translation.StandardTranslationCacheDataLoaderFactory,CoreAppPlatform'
        self._ChangeCoreAppSettingValue(v)

    def B_StartRemotingContainer(self):
        '''开启Remoting Container'''

        rPath = os.path.join(self.prodikaPath,r'Code\Apps\RemotingContainer\bin\RemotingContainer.exe -normal')
        GreenPrint('正在启动...')
        #subprocess.Popen(args=rPath, shell=False)
        os.system(rPath)

p = Prodika()
methods = [i for i in dir(p) if not i.startswith('_') and i[0].isupper()]
print '========================================================='
print '\n请选择需要进行的操作：（按Q退出）\n'
for i in range(len(methods)):
    m = methods[i]
    print str(i) + '. ' + getattr(p,m).__doc__
print '\n========================================================='

selected = ''
while(selected != 'q'):
    YellowPrint('\n请选择序号：')
    selected = raw_input()
    for i in range(len(methods)):
        if selected == str(i):
            getattr(p,methods[i])()
