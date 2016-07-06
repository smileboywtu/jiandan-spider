# -*- coding: utf-8 -*-

# auto proxy from xici.com
# Created: 2016/07/06
# Copyright: (c) 2016<smileboywtu@gmail.com>


import time
import random
import urllib2
from lxml import html
from utils import proxy
from config import globalconstants as constants


class ProxyRobot(object):
    """auto scrape proxy from web"""

    def __init__(self):
        """
        init the robot
        """
        self.handlers = [
            ('http://www.xicidaili.com/nn/', self._get_xici_proxy),
        ]


    @property
    def proxies(self):
        """
        get proxy from default handler config

        :return: proxy list
        """
        proxies = set()

        for url, handler in self.handlers:
            proxies.update(handler(url))

        return list(proxies)


    def _get_xici_proxy(self, url):
        """
        get the proxy list from xici.com

        :param url: url to scrape proxy
        :return: proxy list
        """
        random.seed(time.time())
        req = urllib2.Request(url, headers={'User-Agent': random.choice(constants.USER_AGENTS)})
        page = urllib2.urlopen(req).read()
        parser = html.fromstring(page)

        servers = parser.xpath("//table[@id='ip_list']/tr[position() > 1]/td[position() = 2]/text()")
        ports = parser.xpath("//table[@id='ip_list']/tr[position() > 1]/td[position() = 3]/text()")

        proxies = []
        for server, port in zip(servers, ports):
            proxies.append((server, port))

        return proxies


class ProxyPool(object):
    """manage the proxy"""

    def __init__(self):
        """proxy manager"""
        self._robot = ProxyRobot()
        self.update_proxy()

    @property
    def proxy(self):
        """random choose a proxy from proxies"""
        random.seed(time.time())
        while True:
            _proxy = random.choice(self._proxies)
            http_proxy = proxy.construct_proxy(_proxy)
            if self._check_proxy(http_proxy):
                return http_proxy

    @property
    def proxies(self):
        """get all proxy list"""
        proxies = map(proxy.construct_proxy, self._proxies)
        return proxies

    def update_proxy(self):
        """update proxies"""
        self._proxies = self._robot.proxies

    def _check_proxy(self, proxy):
        """check if the proxy is ok"""
        random.seed(time.time())

        proxy_handler = urllib2.ProxyHandler(proxy)
        opener = urllib2.build_opener(proxy_handler)
        urllib2.install_opener(opener)

        req = urllib2.Request(constants.OFFICIAL_URL, headers={'User-Agent': random.choice(constants.USER_AGENTS)})
        resp = urllib2.urlopen(req, timeout=constants.PROXY_TIMEOUT)
        if resp.getcode() == 200:
            return True
        return False



if __name__ == '__main__':
    pool = ProxyPool()
    print pool.proxy
    #print pool.proxies

