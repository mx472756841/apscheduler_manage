#!/usr/bin/python3
# -*- coding: utf-8

class Middleware(object):
    """
    中间件
    """

    def process_request(self):
        """
        处理请求前处理
        :return:
        """
        raise NotImplementedError
