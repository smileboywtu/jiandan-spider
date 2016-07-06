# -*- coding: utf-8 -*-

# tools for proxy
# Created: 2016-07-05
# Copyright: (c) 2016<smileboywtu@gmail.com>


import urllib2
import gevent.monkey
gevent.monkey.patch_all()


def construct_proxy(proxy):
    """
    construct proxy
    :param proxy: tuple for (server, port)
    :return: http proxy
    """
    http_proxy_value = 'http://{0}:{1}'.format(*proxy)
    http_proxy = {'http': http_proxy_value}
    return http_proxy
