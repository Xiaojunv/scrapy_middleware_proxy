# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import logging

import redis
import requests
from scrapy import signals
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware

from ip_pool.ip_redis import  get_ip
from twisted.internet.error import TimeoutError
r = redis.Redis()


class ProxyMiddleware(object):


    #请求处理
    def process_request(self, request, spider):

        proxy = 'http://' +  get_ip()
        # print(proxy)
        request.meta['proxy'] = proxy
    #报错处理
    def process_exception(self, request, exception, spider):
    #
        print('超时')
        req_ip = request.meta['proxy']
        r.srem('http',req_ip.replace('http://',''))
        #删除写入的代理
        del request.meta['proxy']
        # self.ip = get_ip()
        # proxy = 'http://' + get_ip()
        # request.meta['proxy'] = proxy
        #重新调用请求
        return request


    # #响应处理
    def process_response(self, request, response, spider):
        if response.status == 200:
            return response
        else:
            req_ip = request.meta['proxy']
            r.srem('http', req_ip.replace('http://',''))
            # 删除写入的代理、
            print('响应错误')
            del request.meta['proxy']
            return request