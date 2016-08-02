import os
import errno
import shutil
import logging
import logging.handlers  
import re

def unzipfile(fname):
    fullpath = os.path.join('downloaded',fname)
    if os.system("unzip %s -d pretraindata"%fullpath) == 0:
        logger.info('Success. unzip %s' %fullpath)
    else:
        logger.info('Failed! unzip %s' %fullpath)

def checkjsfile(fname):
    f = open(fname,'r')
    content = f.read()
    if '@param' in content or  '@type' in content or '@arg' in content:
        return True
    return False

def walkjs(fname):
    for dpath,dirs,files in os.walk('pretraindata'):
        for f in files:
            if f.endswith('.js') and os.path.exists(os.path.join(dpath,f)):
                src_path = os.path.join(dpath,f)
                pure_des_path = os.path.join('puredata',f)
                copyandcheckredundancy(src_path,pure_des_path)
                if checkjsfile(src_path):
                    js_des_path = os.path.join('jsdocdata',f)
                    copyandcheckredundancy(src_path,js_des_path)


def copyandcheckredundancy(src_path,des_path):
    redunnum = 0
    while os.path.isfile(getredundancyname(des_path,redunnum)):
        des_content = open(getredundancyname(des_path,redunnum),'r').read()
        src_content = open(src_path,'r').read()
        if des_content == src_content:
            return
        else:
            redunnum += 1
    final_des_path = getredundancyname(des_path,redunnum)
    try:
        shutil.copy(src_path,final_des_path)
        logger.info('Copy: %s to %s'%(src_path,final_des_path))
    except IOError, e:
        logger.info('Failed! Copy: %s to %s'%(src_path,final_des_path))


def getredundancyname(des_path,redunnum):
    if redunnum == 0:
        return des_path
    else:
        return des_path[:-3] + '(' + str(redunnum) + ').js'

def checkproject(fname):
    createdir('pretraindata')
    unzipfile(fname)
    walkjs(fname)
    rmdir('pretraindata')

def walkmain():
    createdir('puredata')
    createdir('jsdocdata')
    for f in os.listdir('downloaded'):
        if f.endswith('.zip'):
            checkproject(f)

def createdir(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(path):
            logger.info ('%s existed'%path)
            pass
        else: 
            raise e

def rmdir(path):
    shutil.rmtree(path)

if __name__ == '__main__':
    LOG_FILE = 'jsdocproject_searcher.log'  
    fh = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024, backupCount = 5)
    sh = logging.StreamHandler()
    fmt = '%(asctime)s - %(message)s'  
    formatter = logging.Formatter(fmt)  
    fh.setFormatter(formatter) 
    sh.setFormatter(formatter) 
    logger = logging.getLogger('jsdocproject_searcher')
    logger.addHandler(fh)
    logger.addHandler(sh) 
    logger.setLevel(logging.INFO) 
    walkmain()
