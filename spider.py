'''
https://www.autohome.com.cn/all/
https://www.autohome.com.cn/all/2/#liststart
文章：
    title
    summary
    a_url
    img_url
    tags

pip install requests
pip install beautifulsoup4
'''

import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor


def work(k):
    response = requests.get(url='https://www.autohome.com.cn/all/{}/#liststart'.format(k))
    # print(response.headers)
    # print(response.encoding)
    # print(response.status_code)
    # print(response.text)
    response.encoding = 'GBK'
    soup_obj = BeautifulSoup(response.text, 'html.parser')
    div_obj = soup_obj.find(name='div', attrs={"id": "auto-channel-lazyload-article"})
    # print(div_obj)
    li_list = div_obj.find_all(name="li")
    # count = 1
    for i in li_list:
        title_obj = i.find(name='h3')
        if not title_obj: continue
        title = title_obj.text
        summary = i.find(name='p').text
        a = 'https:' + i.find(name='a').get('href')
        image = 'https' + i.find(name='img').get('src')
        tags = a.split('/', 4)[3]
        # print('start %s' % count + '*' * 100)
        # print('title : ' + title)
        # print('summary : ' + summary)
        # print('a : ' + a)
        # print('image : ' + image)
        # print('tags : ' + tags)
        # print('end %s' % count + '*' * 100)
        print(response.url, title, tags)
        print()
        # count += 1


def spider():
    """ 爬取汽车之家 """
    t = ThreadPoolExecutor(10)
    for k in range(1, 10):
        t.submit(work, k)
    t.shutdown()


if __name__ == '__main__':
    import time

    start = time.time()
    spider()
    print(time.time() - start)
