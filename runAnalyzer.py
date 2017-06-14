import logging
import os
from pathlib import Path

from LinkAnalizer import LinkAnalizer
from LinkDownloader import LinkDownloader

FORMAT = '%(asctime)-15s - %(threadName)s - %(name)s - %(levelname)s - %(message)s'
log_file = str(Path(os.getcwd()) / 'logs_analyze.txt')
logging.basicConfig(filename=log_file, level=logging.INFO, format=FORMAT)
logger = logging.getLogger('Main')


LinkDownloader.cache_dir = 'cache_cam_html'
LinkDownloader.cache_location = '/media/marek/data'
# root = 'http://www.ox.ac.uk/'
root = 'https://www.cam.ac.uk/'

logger.error('start')

a = LinkAnalizer(root)
a.analize()
# print (len(a.visited))
# print (len(a.hit))

logger.error('end')