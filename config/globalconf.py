# -*- coding: utf-8 -*-

# Global Config File
# Created: 2016-07-06
# Copyright: (c) 2016<smileboywtu@gmail.com>


import os

HOME = os.environ['HOME']

# set the image save directory
IMAGE_FILE_DIR = os.path.join(HOME, 'images')

# set the request config
REQ_TIMEOUT = 25

START_PAGE = 650 # when set this you should go to jiandan.com to see the max tab value
PAGE_DELTA = 10

# set jiandan http concurrent load
HTTP_CONCURRENT_LOAD = 1000 # no more than 1024

# auto proxy
AUTO_PROXY = False