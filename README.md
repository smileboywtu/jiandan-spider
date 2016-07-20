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
python spider.py
```

Before you run the script, you should setup the spider in the `config/globalconf.py` file:

``` python2

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

```

# Lisence

MIT
