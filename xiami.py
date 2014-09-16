#coding: UTF-8
import urllib2
import urllib
import re
import string
from bs4 import BeautifulSoup

#获取html
def getthehtml(url):
        request = urllib2.Request(url)
        request.add_header('User-Agent', 'Mozilla')
        response = urllib2.urlopen(request)
        return response
#解码mp3地址
def decode():
    _len = len(location[1:])
    key = int(location[0])
    line= _len / key
    right_line = _len % key
    new_url = location[1:]
    ture_url = ''

    for i in xrange(_len):
        a = i % key
        b = i / key
        c = 0
        if a <= right_line:
            c = a * (line + 1) + b
        else:
            c = right_line * (line + 1) + (a - right_line) * line + b
        ture_url += new_url[c]
    return urllib2.unquote(ture_url).replace('^', '0')
#主程序
if __name__ == "__main__":
    song_name =raw_input ('please input the song\'s name')
    url_search = 'http://www.xiami.com/search?%s'%(urllib.urlencode({'key': song_name}))
    soup_search = BeautifulSoup(getthehtml(url_search))
    html = soup_search.findAll(class_ = re.compile("song_name"))[1]

    src =  html.a
    _url = src.get('href')
    song_name = src.get('title')
    print _url, song_name
    song_id = re.search(r'(?<=song\/).*(?=)', _url).group()
    soup = BeautifulSoup(getthehtml(_url))
    foundlyr = soup.findAll(class_=re.compile("lrc_main"))
    foundinfo = soup.findAll(class_=re.compile("album_relation"))
    url1 = 'http://www.xiami.com/song/playlist/id/%s/object_name/default/object_id/0'%song_id

    resp = getthehtml(url1).read()
    lyricurl=re.search(r'(?<=\<lyric\>).*(?=\<\/lyric\>)',resp).group()
    location=re.search(r'(?<=\<location\>).*?(?=\<\/location\>)',resp).group()
    print 'the song has begun downloading.'
    urllib.urlretrieve(decode(), song_name+'.mp3')
    lyricurl = 'lyric\'s url is %s /n'%lyricurl
    location = 'location\'s url is %s'%decode()
    f=open(song_name+'.html' ,'w')
    print >>f,foundinfo,foundlyr,lyricurl,location
    f.close()
    print  location
    print  'MISSION ACCOMPLISHED'




