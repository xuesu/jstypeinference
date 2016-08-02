import os
import errno
import shutil
import logging
import logging.handlers 

def createdir(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(path):
            logger.info ('%s existed'%path)
            pass
        else: 
            raise e

def walkjsnice():
    createdir('jsnicedata')
    for dpath,dirs,files in os.walk('jsdocdata'):
        for f in files:
            src_path = os.path.join(dpath,f)
            des_path = os.path.abspath(os.path.join('jsnicedata',f))
            os.system('java -jar /home/iris/workspace/jsnice/compiler.jar --compilation_level=JSNICE '+
             '--jsnice_infer=TYPES --jsnice_features=TYPEREL,TYPEALIAS,TYPERELALIAS ' + 
             '%s > %s'%(src_path,des_path))
            logger.info('jsnice %s > %s'%(src_path,des_path))

if __name__ == '__main__':
    LOG_FILE = 'jsniceresult_getter.log'  
    fh = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024, backupCount = 5)
    sh = logging.StreamHandler()
    fmt = '%(asctime)s - %(message)s'  
    formatter = logging.Formatter(fmt)  
    fh.setFormatter(formatter) 
    sh.setFormatter(formatter) 
    logger = logging.getLogger('jsniceresult_getter')
    logger.addHandler(fh)
    logger.addHandler(sh) 
    logger.setLevel(logging.INFO) 
    walkjsnice()