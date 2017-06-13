import logging


from LinkAnalizer import LinkAnalizer
from LinkDownloader import LinkDownloader

FORMAT = '%(asctime)-15s - %(threadName)s - %(name)s - %(levelname)s - %(message)s'
log_file = "C:\\Users\\mareczek\\PycharmProjects\\mi_2_robot\\logs_analize.txt"
logging.basicConfig(filename=log_file, level=logging.INFO, format=FORMAT)
logger = logging.getLogger('Main')


LinkDownloader.cache_dir = 'cache_cam_html2'
# root = 'http://www.ox.ac.uk/'
root = 'https://www.cam.ac.uk/'

logger.error('start')

a = LinkAnalizer(root)
a.analize()
print (len(a.visited))
print (len(a.hit))

logger.error('end')