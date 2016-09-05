#!/usr/bin/python
# -*- coding:utf-8 -*-

import urllib
import urllib2
import json
import os
import hashlib


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


def http_post(szFilePath, lang):
    url = 'https://www.shooter.cn/api/subapi.php'
    filehash = ComputerFileHash(szFilePath)
    values = {'filehash': filehash, 'pathinfo': szFilePath, 'format': 'json', 'lang' : lang}
    values = urllib.urlencode(values)
    req = urllib2.Request(url, values)
    response = urllib2.urlopen(req)
    text = response.read()
    return text


if __name__ == '__main__':
    szFilePath = 'D:\\The.Secret.Life.of.Walter.Mitty.2013.720p.BluRay.x264-SPARKS.mkv'
    print json.loads(http_post(szFilePath, 'Chn'))
