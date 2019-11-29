# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponse
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from web import models
import time
from django.http.response import JsonResponse
import json
from multiprocessing import cpu_count

es = Elasticsearch(["localhost"], http_auth=('elastic', 'wangzb'), port=9210, timeout=50000)
'''
sudo pip install mysqlclient
python manage.py migrate   # 创建表结构
python manage.py makemigrations TestModel  # 让 Django 知道我们在我们的模型有一些变更
python manage.py migrate web   # 创建表结构,如果要修改表结构，重新修改Article，再次执行
'''


def search_suggest(search_msg):
    body = {
        "suggest": {
            "index_python_test3": {
                "text": search_msg,
                "completion": {
                    "field": "title",
                    "size": 6
                }
            }
        }
    }
    res = es.search(index="index_python_test3", body=body)

    try:
        l2 = [i['text'] for i in res['suggest']['index_python_test3'][0]['options']]
        # l2 = [i['highlighted'] for i in res['suggest']['index_python_test2'][0]['options']]
        print(l2)
    except Exception as e:
        l2 = []
    return l2


def suggest(request):
    if request.method == 'POST':
        search_msg = request.POST.get("search_msg")
        res = search_suggest(search_msg)
        return JsonResponse(res, safe=False)
    else:
        return render(request, 'index.html')

    # if request.method == 'GET':
    #     flag = request.GET.get('flag', 'aaa')
    #     if flag == 'aaa':
    #         obj = models.Article.objects.filter(pk__lte=100)
    #         return render(request, 'index.html', {'all_obj': obj})
    #     else:
    #         search_msg = request.GET.get('search_msg')
    #         action_type = request.GET.get('action_type')
    #         res = filter_msg(search_msg, action_type)
    #         return JsonResponse(res)
    # else:
    #     search_msg = request.POST.get("search_msg")
    #     action_type = request.POST.get("action_type")
    #     res = filter_msg(search_msg, action_type)
    #     return JsonResponse(res)


def filter_msg(search_msg, action_type):
    if action_type == 'all':
        body = {
            "size": 10,
            "query": {
                "match": {
                    "title": search_msg
                }
            },
            "highlight": {
                "pre_tags": "<b style='color:red;'>",
                "post_tags": "</b>",
                "fields": {
                    "title": {}
                }
            }
        }
    else:
        body = {
            "size": 10,
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "title": search_msg
                            }
                        },
                        {
                            "match": {
                                "tags": action_type
                            }
                        }
                    ]
                }
            },
            "highlight": {
                "pre_tags": "<b style='color:red;'>",
                "post_tags": "</b>",
                "fields": {
                    "title": {}
                }
            }
        }

    res = es.search(index="index_python_test3", body=body)
    return res


def index(request):
    """ 首页 """
    # if request.method == 'POST':
    #     search_msg = request.POST.get("search_msg")
    #     res = filter_msg(search_msg)
    #     return JsonResponse(res)
    # else:
    #     res = get_msg(request)
    #     return res
    if request.method == 'GET':
        flag = request.GET.get('flag', 'aaa')
        if flag == 'aaa':
            obj = models.Article.objects.filter(pk__lte=100)
            return render(request, 'index.html', {'all_obj': obj})
        else:
            search_msg = request.GET.get('search_msg')
            action_type = request.GET.get('action_type')
            res = filter_msg(search_msg, action_type)
            return JsonResponse(res)
    else:
        search_msg = request.POST.get("search_msg")
        action_type = request.POST.get("action_type")
        res = filter_msg(search_msg, action_type)
        return JsonResponse(res)


def work(k):
    # k页数
    response = requests.get(url='https://www.autohome.com.cn/all/{}/#liststart'.format(k))
    response.encoding = 'GBK'
    soup_obj = BeautifulSoup(response.text, 'html.parser')
    div_obj = soup_obj.find(name='div', attrs={"id": "auto-channel-lazyload-article"})
    li_list = div_obj.find_all(name="li")
    for i in li_list:
        title_obj = i.find(name='h3')
        if not title_obj: continue
        title = title_obj.text
        summary = i.find(name='p').text
        a = 'https:' + i.find(name='a').get('href')
        image = 'https' + i.find(name='img').get('src')
        tags = a.split('/', 4)[3]
        article = models.Article(title=title, summary=summary, a_url=a, img_url=image, tags=tags)
        article.save()


def spider():
    """ 爬取汽车之家的数据存入MySql """
    t = ThreadPoolExecutor(cpu_count() * 5)
    for k in range(1, 6000):
        t.submit(work, k)
    # t.shutdown 对所有线程执行完返回
    # t.shutdown()
    return HttpResponse("OK")


def es_sync_data(request):
    """ MySql汽车之家的数据同步到Es """
    body = {
        "mappings": {
            "doc": {
                "properties": {
                    "title": {
                        "type": "completion",
                        "analyzer": "ik_smart"
                    },
                    "summary": {
                        "type": "text"
                    },
                    "a_url": {
                        "type": "keyword"
                    },
                    "img_url": {
                        "type": "keyword"
                    },
                    "tags": {
                        "type": "text"
                    }
                }
            }
        }
    }
    # 查看该index是否存在
    # print(es.indices.exists(index='index_python_test2'))
    # 新增index
    es.indices.create(index='index_python_test3', body=body)
    # 验证index
    # print(es.indices.get_mapping(index='index_python_test2'))
    query_obj = models.Article.objects.all()
    action = (
        {
            "_index": "index_python_test3",
            "_type": "doc",
            "_source": {
                "title": i.title,
                "summary": i.summary,
                "a_url": i.a_url,
                "img_url": i.img_url,
                "tags": i.tags
            }
        } for i in query_obj)
    s = time.time()
    helpers.bulk(es, action)
    print(time.time() - s)
    return HttpResponse('OK')

# if __name__ == '__main__':
#     start = time.time()
#     spider()
#     print(time.time() - start)
