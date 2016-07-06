# -*- coding: utf-8 -*-

# tools for proxy
# Created: 2016-07-05
# Copyright: (c) 2016<smileboywtu@gmail.com>


from config import globalconf as conf


def slice(urls):
    """
    slice the urls according to the http concurrent load
    :param urls: request urls
    :return: generator
    """
    start = 0
    stop = start + conf.HTTP_CONCURRENT_LOAD

    while stop < len(urls):
        yield urls[start:stop]
        start = stop
        stop += conf.HTTP_CONCURRENT_LOAD

