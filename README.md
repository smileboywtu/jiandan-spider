# Jiandan Spider

Scrape jiandan/ooxx images and save to file system.

This is a demo:

![Alt text](./screenshot/demo.png)

# Feature

This program powered by python 2.7.

Support:

1. Auto Proxy
2. HTTP REQUEST Load Setting
3. Multiple Page Scrape

# Requirements

+ lxml
+ gevent

# How-To

Just run the spider.py

``` shell
#!/bin/bash
python spider.py
```

Before you run the script, you should setup the spider in the `config/globalconf.py` file:

``` python

#!/usr/bin/env python
# -*- coding: utf-8 -*-

HOME = os.environ['HOME']

# set the image save directory
IMAGE_FILE_DIR = os.path.join(HOME, 'images')

# set the request config
REQ_TIMEOUT = 25

START_PAGE = 650 # when set this you should go to jiandan.com to see the max tab value
PAGE_DELTA = 10

# set jiandan http concurrent load
HTTP_CONCURRENT_LOAD = 1000 # no more than 1024

```

There are some commandline arguments you can use to control the spider:

``` shell
#!/bin/bash
usage: spider.py [-h] [-s START] [-d DELTA] [-p PROXY]

set scrap page start number, page scrape number

optional arguments:
  -h, --help            show this help message and exit
  -s START, --start START
                        Scrape start page, the minimux number is 0.
  -d DELTA, --delta DELTA
                        Scrape page numbers, the minimux number is 1.
  -p PROXY, --proxy PROXY
                        Enable auto-proxy.
```

# Lisence

MIT
