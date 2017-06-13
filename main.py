import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import os

from pathlib import Path
from urllib.parse import urljoin, urlparse

from Executor import Executor
from LinkChecker import LinkChecker
from LinkDownloader import LinkDownloader
import logging

#from LinkManager import LinkManager
from LinkExtractor import LinkExtractor
from LinkProcessor import LinkProcessor

FORMAT = '%(asctime)-15s - %(threadName)s - %(name)s - %(levelname)s - %(message)s'
log_file = "C:\\Users\\mareczek\\PycharmProjects\\mi_2_robot\\logs.txt"
#os.remove(log_file)
logging.basicConfig(filename=log_file, level=logging.INFO, format=FORMAT)
#logging.basicConfig(level=logging.INFO, format=FORMAT)
logger = logging.getLogger('Main')

# root = 'https://www.python.org/'
root = 'https://www.cam.ac.uk/'
# root = 'http://www.ox.ac.uk/'

LinkDownloader.cache_dir = 'cache_cam_html2'

executor = Executor(root, 100, 1)
executor.work()


# checker = LinkChecker(root)
# manager = LinkManager()

# processor = LinkProcessor(root, checker, manager)


# def processAndAddTasks(tasks, executor):
#     for p in tasks:
#         logger.info('new task to queue thread: {0} link: {1}'.format(threading.get_ident(), p.link))
#         print('new task to queue thread: {0} link: {1}'.format(threading.get_ident(), p.link))
#     future_to_url = { executor.submit(lambda : p.process(3)) : p.link for p in tasks }
#     for future in as_completed(future_to_url):
#         link = future_to_url[future]
#         new_tasks = []
#         try:
#             new_tasks = future.result()
#         except Exception as exc:
#             print('%r generated an exception: %s' % (link, exc))
#         else:
#             f = executor.submit(processAndAddTasks, new_tasks, executor)
#             f.result()
#
# with ThreadPoolExecutor() as executor:
#     future = executor.submit(processAndAddTasks, [processor], executor)
#     future.result()

#tasks = [processor]
#done = 0
#while done < len(tasks) and done < 20:
    # task = tasks[done]
    # done += 1
    # new_tasks = task.process()
    # for n_task in new_tasks:
    #     tasks.append(n_task)



# print(links.domain_url)
# print(links.robots_url)


#d = LinkDownloader(root)
#d.load_data()

#root_url = urlparse(root)

#extractor = LinkExtractor()
#for url in extractor.get_good_links_from_data(d.data, root, checker):
        #print(url)



# print(d.data)