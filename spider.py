#!/usr/bin/env python

# scrape web image url
# Created: 2016-07-05
# Copyright: (c) 2016<smileboywtu@gmail.com>


import os
import time
import random
import pprint
import urllib2
import argparse
from lxml import html
from string import Template

from config import globalconf as conf
from config import globalconstants as constants

from freeproxy import autoproxy
from executor.http_pool import HttpPool

import gevent
# use gevent socket
import gevent.monkey
gevent.monkey.patch_all()


def set_proxy_openner(http_proxy):
    """
    set the global urllib2 proxy opener
    :param http_proxy: http proxy
    :return: None
    """
    proxy_handler = urllib2.ProxyHandler(proxies=http_proxy)
    opener = urllib2.build_opener(proxy_handler)
    urllib2.install_opener(opener)


def setup_proxy():
    """
    setup global proxy
    :return:
    """
    proxy_pool = autoproxy.ProxyPool()
    set_proxy_openner(proxy_pool.proxy)


def construct_req(url):
    """
    construct the req use url

    :param url: url to construct
    :return: urllib2 req
    """
    random.seed(time.time())
    req = urllib2.Request(url, headers={'User-Agent': random.choice(constants.USER_AGENTS)})
    return req


def generate_url(url_template, number):
    """
    construct scrapy source urls

    :param url_template: url template for jiandan
    :param number: jiandan.com source tab range
    :return: scrapy urls
    """
    urls = []
    start, delta = number
    for index in xrange(start, start+delta):
        urls.append(Template(url_template).safe_substitute(num=index))
    return urls


def get_image_url(urls):
    """
    get image url from the page source

    :param urls: page source url
    :return: image urls
    """
    executor = HttpPool(conf.HTTP_CONCURRENT_LOAD, scrape_image)
    executor.add_tasks(urls)
    images = executor.run()
    return list(set(images))


def scrape_image(url):
    """
    scrapy the image url from the page source

    :param url: page url
    :return: image urls list
    """
    req = construct_req(url)
    page = urllib2.urlopen(req).read()
    parser = html.fromstring(page)
    urls = parser.xpath("//*[@id='comments']/ol[@class='commentlist']/li//img/@src")
    return urls


def download_image(urls):
    """
    download the image from given urls

    :param urls: image urls
    :return: None
    """
    counter = 0

    # check dir
    if not os.path.isdir(conf.IMAGE_FILE_DIR):
        os.mkdir(conf.IMAGE_FILE_DIR)

    def _download(url):
        req = construct_req(url)
        resp = urllib2.urlopen(req, timeout=conf.REQ_TIMEOUT)
        if resp.getcode() == 200:
            # path construct
            filename = url.split('/')[-1]
            path = os.path.join(conf.IMAGE_FILE_DIR, filename)
            with open(path, 'wb') as fp:
                fp.write(resp.read())
            return 1
        return 0

    executor = HttpPool(conf.HTTP_CONCURRENT_LOAD, runner=_download)
    executor.add_tasks(urls)
    resp = executor.run()
    for val in resp:
         try:
             counter += val
         except TypeError:
             pass
    print 'image download process done, %d images downloaded and saved to %s' % (counter, conf.IMAGE_FILE_DIR)


def command_line():
    """
    get user arguments

    :return: args
    """
    parser = argparse.ArgumentParser(description='set scrap page start number, page scrape number')
    parser.add_argument('-s', '--start', help='Scrape start page, the minimux number is 0.')
    parser.add_argument('-d', '--delta', help='Scrape page numbers, the minimux number is 1.')
    args = parser.parse_args()
    return args


def main():
    """
    main func

    :return: None
    """
    args = command_line()
    start = args.start or conf.START_PAGE
    delta = args.delta or conf.PAGE_DELTA

    if conf.AUTO_PROXY:
        setup_proxy()
        print 'setup proxy ok...'
    urls = generate_url(constants.URL_TEMPLATE, (start, delta))
    print 'scrape page urls: '
    pprint.pprint(urls)
    images = get_image_url(urls)

    print '%d images will be download. they are: ' % len(images)
    pprint.pprint(images)
    print 'start to download image...'
    download_image(images)


if __name__ == '__main__':
    main()
