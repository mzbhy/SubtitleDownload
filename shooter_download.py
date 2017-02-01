#!/usr/bin/python
# -*- coding:utf-8 -*-
# API说明：https://docs.google.com/document/d/1ufdzy6jbornkXxsD-OGl3kgWa4P9WO5NZb6_QYZiGI0/preview#


"""通过射手API自动获取并下载字幕文件

Usage:
    shooter_download [-cer] <szFilePath>

Options:
    -h,--help        显示帮助菜单
    -c               中文字幕(默认)
    -e               英文字幕
    -r               递归下载(默认不递归)

Example:
    shooter_download D:\test.avi
    shooter_download -c D:\test.avi
    shooter_download -r D:\videos
"""

import urllib
import urllib2
import json
import os
import hashlib
import sys
import platform
import mimetypes
from docopt import docopt

reload(sys)
sys.setdefaultencoding( "utf-8" )


def isWindowsSystem():
    return 'Windows' in platform.system()
 
def isLinuxSystem():
    return 'Linux' in platform.system()

def ComputerFileHash(szFilePath):
    file_object = open(szFilePath, 'rb')
    FileSize = 0L
    offsets = [0 for i in range(4)]
    szRet = ''
    try:
        FileSize = os.path.getsize(szFilePath)
        if(FileSize < 8192):
            #a video file less then 8k? impossible!
            pass
        else:
            offsets[3] = FileSize - 8192
            offsets[2] = FileSize / 3
            offsets[1] = FileSize / 3 * 2
            offsets[0] = 4096
            for offset in offsets:
                file_object.seek(offset, 0)
                data = file_object.read(4096)
                szMD5 = hashlib.md5(data)
                if szRet:
                    szRet += ';'
                szRet += str(szMD5.hexdigest())
    finally:
        file_object.close( )
    return szRet


def get_sub_address(szFilePath, languages):
    url = 'https://www.shooter.cn/api/subapi.php'
    sublist = []
    if os.path.exists(szFilePath):
        filehash = ComputerFileHash(szFilePath)
        for lang in languages:
            values = {'filehash': filehash, 'pathinfo': szFilePath, 'format': 'json', 'lang' : lang}
            values = urllib.urlencode(values)
            try:
                req = urllib2.Request(url, values)
                response = urllib2.urlopen(req)
                text = response.read()
                if text == '\xff':
                    pass
                else:
                    sublist = sublist + (json.loads(text))
            except:
                print u'网络连接错误！'
                exit()
        return sublist
    else:
        print u'文件路径错误！'
        exit()


def download_sub(szFilePath, sublist):
    path = os.path.dirname(szFilePath)
    if sublist:
        print u'找到了 %d 个字幕文件！' % len(sublist)
        number = 0
        for subjson in sublist:
            download_url = subjson['Files'][0]['Link']
            sub_ext = '.' + subjson['Files'][0]['Ext']
            req = urllib2.Request(download_url)
            response = urllib2.urlopen(req)
            number += 1
            filename = response.info()['Content-Disposition'].split('filename=')[1].rstrip(sub_ext) + '(' + str(number) + ')' + sub_ext
            print u'正在下载第 %d 个字幕' % number
            if isWindowsSystem():
                urllib.urlretrieve(download_url, filename)
            if isLinuxSystem():
                urllib.urlretrieve(download_url, path + '/' + filename)
        print u'下载完成！'
    else:
        print u'没有找到字幕！'

def download_sub_dir(szFilePath, languages, recursive):
    if recursive:
        g = os.walk(szFilePath)  
        for path, d, filelist in g:  
            for f in filelist:  
                filename = os.path.join(path, f)
                types = mimetypes.guess_type(filename)
                mtype = types[0]
                if mtype is not None and mtype.split('/')[0] == 'video':
                    print u'正在处理:' + filename
                    download_sub(filename, get_sub_address(filename, languages))
    else:
        for file in os.listdir(szFilePath):
            filename = os.path.join(szFilePath, file)
            if os.path.isfile(filename):
                types = mimetypes.guess_type(filename)
                mtype = types[0]
                if mtype is not None and mtype.split('/')[0] == 'video':
                    print u'正在处理:' + filename
                    download_sub(filename, get_sub_address(filename, languages))


def main():
    """command-line interface"""
    arguments = docopt(__doc__)
    szFilePath = arguments['<szFilePath>'].decode('GB2312')
    if arguments['-c'] and arguments['-e']:
        lang = ['eng', 'chn']
    elif arguments['-e']:
        lang = ['eng']
    else:
        lang = ['chn']
    if arguments['-r']:
        recursive = True
    else:
        recursive = False
    if os.path.isdir(szFilePath):
        download_sub_dir(szFilePath, lang, recursive)
    else:
        download_sub(szFilePath, get_sub_address(szFilePath, lang))


if __name__ == '__main__':
    main()
