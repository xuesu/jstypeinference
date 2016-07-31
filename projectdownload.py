import urllib
import os
import errno
import logging  
import logging.handlers  
from lxml import etree
import time

def crawl(lang_name,p_max):
    logger.info('crawling %d %s projects',p_max,lang_name)
    page_max = int((p_max + 9) / 10)
    p = 0
    createdownloadeddir()
    for page in range(1,page_max + 1):
        tmp = crawlpage(lang_name,page,p,p_max)
        if tmp <= 0 or p >= p_max:
            break
        p += tmp
    logger.info("download %d %s projects."%(p,lang_name))
    return p

def  crawlpage(lang_name,page,p_now,p_max):
    params = urllib.urlencode({'l':lang_name,'p':page,'q':'language:%s' % lang_name,'type':'Repositories'})
    url_str = "https://github.com/search?%s" % params
    logger.info ('crawling:%s' % url_str)
    f = urllib.urlopen(url_str)
    content = f.read()
    if content == '' or content == None:
        return -1
    root = etree.HTML(content)
    href_list = root.xpath("//h3[@class='repo-list-name']/a/@href")
    p = 0
    for href_str in href_list:
        if p + p_now< p_max:
            if crawlproject(href_str):
                p = p + 1
    logger.info("download %d projects in %s."%(p,url_str))
    return p
#https://github.com/montylounge/django-mingus/archive/master.zip

def downloadproject(url_str,local_path,t):
    try:
        urllib.urlretrieve(url_str,local_path)
    except urllib.ContentTooShortError:
        if t <= 5:
            logger.info ('Network conditions is not good.Reloading.')
            time.sleep(0.1*t*t)
            downloadproject(url_str,local_path,t+1)
        else:
            logger.info ('Poor connection! download %s ' % url_str)
            return False
    except Exception:
        logger.info ('Failed! download %s ' % url_str)
        return False
    logger.info ('Success! download %s' % url_str)
    return True

def crawlproject(href_str):
    urlpattern = "https://github.com%s/archive/master.zip"
    url_str = urlpattern % href_str
    logger.info ('downloading %s' % url_str)
    file_name = href_str.replace('/','_')
    file_name += '_master.zip'
    local_path = os.path.join('downloaded',file_name)
    if os.path.isfile(local_path):
        logger.info("%s existed"%local_path)
        return True
    return downloadproject(url_str,local_path,0)

def createdownloadeddir():
    path = 'downloaded'
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(path):
            logger.info ('downloaded existed')
            pass
        else: 
            raise e

if  __name__ == '__main__':
    LOG_FILE = 'github_crawler.log'  
    fh = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024, backupCount = 5)
    sh = logging.StreamHandler()
    fmt = '%(asctime)s - %(message)s'  
    formatter = logging.Formatter(fmt)  
    fh.setFormatter(formatter) 
    sh.setFormatter(formatter) 
    logger = logging.getLogger('github_crawler')
    logger.addHandler(fh)
    logger.addHandler(sh) 
    logger.setLevel(logging.INFO)  
    lang_name= raw_input("please input the langauge  of those projects that you want to crawl:")
    p_max = input("please input the maximum of projects number you want to crawl:")
    crawl(lang_name,p_max)
