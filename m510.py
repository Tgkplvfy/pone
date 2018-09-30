# coding: utf-8
import requests
from bs4 import BeautifulSoup
import time
import os
from urllib.request import urlretrieve
import pymysql,random
from requests.exceptions import ReadTimeout,ConnectionError,RequestException,HTTPError

main_url = "http://www.m510.com"
start_url = "http://www.m510.com/zhonghefuli/"
my_ua = ["Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36","Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0""Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14","Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)"]
ua = random.choice(my_ua)
header = {
    'User-Agent': ua,
    'Host': 'www.m510.com',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate'


}

#定义一个请求
def get_content(url):
    try:
        response = requests.get(url,headers=header)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content,'lxml')
            return soup
    except ReadTimeout:
        print('网络超时')
        time.sleep(30)
        get_content(url)
    except ConnectionError:
        print('网络错误')
        time.sleep(30)
        get_content(url)
    except HTTPError:
        print('错误code')
        time.sleep(30)
        get_content(url)
    except RequestException:
        print('请求错误')
        time.sleep(60)
        get_content(url)


#获取列表
def get_list(url):
    list_content = get_content(url)
    soup = list_content.select('ul.ui-grid-trisect li')
    for li in soup:
        #img_url = li.select('a')[0].select('img')[0].get('src')
        #name = li.select('a')[1].text
        detail_url = main_url + li.select('a')[1].get('href')
        time.sleep(1)
        get_detail(detail_url)

    #print(soup)

#获取详情页内容
def get_detail(url):
    time.sleep(1)
    detail_content = get_content(url)
    try:
        video_url = detail_content.select('source')[0].get('src')
        title = detail_content.select('title')[0].string
        img_url = detail_content.select('video')[0].get('poster')
        print(img_url)
        file_download(url,img_url)
        print('文件已下载！')
        print(url)
        time.sleep(1)
        file_download(url,video_url)
        print('视频下载完成！')

        conn = pymysql.connect(host='localhost',user='root',password='root',db='kansizu',charset='utf8')
        cur = conn.cursor()

        #insert mysql
        sql = "INSERT INTO kansizu(`title`,`img_url`,`video_url`) VALUES('%s','%s','%s')" % (title,img_url,video_url)
        #print(sql)
        try:
            cur.execute(sql)
            conn.commit()
        except:
            print('插入数据错误！')
        conn.commit()
        cur.close()
        conn.close()
    except IndexError:
        print('链接错误：%s' % url)
    
    #download video
    #download img

def file_download(detail_url,f):
    dir_name = detail_url.split('/',5)[4]
    dir_path = "e:/m510/"+dir_name
    isExists = os.path.exists(dir_path)
    file_name = f.split('/')[-1]
    if not isExists:
        os.makedirs(dir_path)

    file_path = os.path.join(dir_path,file_name)
    try:
        urlretrieve(f,file_path)
    except:
        time.sleep(10)
        print('下载失败：%s' % f)



if __name__ == '__main__':
    print('xx')
    #get_detail(start_url)
    #response = requests.get(start_url)
    
    #获取总页数
    response = get_content(start_url)
    total_page = response.select('span.pageinfo strong')[0].string
    for i in range(int(total_page)):
        url = "http://www.m510.com/zhonghefuli/list_4_"+str(i+11)+".html"
        cur_page = '当前第'+str(i+49)+'页。'
        print(cur_page)
        get_list(url)
    #print(soup)
