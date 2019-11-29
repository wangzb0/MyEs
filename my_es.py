'''
pip install elasticsearch
'''
from elasticsearch import Elasticsearch
from elasticsearch import helpers

es = Elasticsearch(["localhost"], http_auth=('elastic', 'wangzb'), port=9210, timeout=50000)
# print(es.ping())

# 创建/修改文档
# print(es.index(index='index_python_test1', doc_type="python", id=1, body={"content": "使用python创建es索引"}))
# 查询
# print(es.get(index='index_python_test1', doc_type="python", id=1))
# 删除
# print(es.delete(index='index_python_test1', doc_type="python", id=1))

# body = {
#     "query": {
#         "match": {
#             "content": "使用python创建es索引"
#         }
#     }
# }
# print(es.search(index="index_python_test1", body=body))
# print(es.search(index="index_python_test1", body=body, filter_path=['hits.hits']))
# print(es.search(index="index_python_test1", body=body, filter_path=['hits.hits._source']))
# print(es.search(index="index_python_test1", body=body, filter_path=['hits.hits._source', 'hits.total']))
# print(es.search(index="index_python_test1", body=body, filter_path=['hits.*']))
# print(es.search(index="index_python_test1", body=body, filter_path=['hits.hits._*']))

# 循环添加文档
# for i in range(1, 11):
#     print(es.index(index='index_python_test1', doc_type='python', body={'name': 'wang%s' % i}))

# 查询数量
# print(es.count(index='index_python_test1', doc_type='python', body={
#     "query": {
#         "match": {
#             "content": "使用python创建es索引"
#         }
#     }
# }))

# 条件删除
# print(es.delete_by_query(index='index_python_test1', body={
#     "query": {
#         "match": {
#             "content": "使用python创建es索引"
#         }
#     }
# }))

# es基础信息
# print(es.info())

# 查看es的某个数据库的当前状态
# print(es.cat.indices(index='index_python_test1'))

# 关闭es的某个数据库
# print(es.indices.close(index='index_python_test1'))

# 打开es的某个数据库
# print(es.indices.open(index='index_python_test1'))

# 查询es集群设置
# print(es.cluster.get_settings())

# 查询es集群运行状况
# print(es.cluster.health())

# 查询整个集群的综合状态信息
# print(es.cluster.state())

# 返回群集当前节点的信息
# print(es.cluster.stats())

# key value     格式输出
# print(es.cat.count(format='json'))



# actions = (
#         {
#             "_index": "my_suggest",
#             "_type": "doc",
#             "_source": {
#                 "title": i.title
#             }
#         } for i in f)
#
# helpers.bulk(es,actions=actions)