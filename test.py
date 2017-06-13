from urllib.parse import urlparse, urldefrag
from urllib.request import urlopen, Request, HTTPSHandler, build_opener, install_opener
# from urllib.robotparser import RobotFileParser
import ssl
#
#https_handler = HTTPSHandler(context=ssl._create_unverified_context())
#opener = build_opener(https_handler)
#install_opener(opener)
#
# rp = RobotFileParser()
# rp.set_url('https://www.cam.ac.uk/robots.txt')
# rp.read()
#
# print(rp.can_fetch('*', 'https://www.cam.ac.uk/'))
from LinkDownloader import LinkDownloader
from LinkExtractor import LinkExtractor
from LinkManager import LinkManager

logfile = "C:\\Users\\mareczek\\PycharmProjects\\mi_2_robot\\logs.txt"

def test_already():
    l = []
    with (open(logfile, "r")) as f:
        lines = f.readlines()
        for line in lines:
            if 'already' in line:
                split = line.split(' ')
                l.append(split[17].rstrip())
                print(split)

    seen = set()
    uniq = [x for x in l if x not in seen and not seen.add(x)]

    print(len(seen))
    print(len(uniq))

def test_proc():
    l = []
    with (open(logfile, "r")) as f:
        lines = f.readlines()
        for line in lines:
            if 'LinkProcessor' in line and 'skipping' not in line:
                split = line.split(' ')
                l.append(split[17].rstrip())
                #print(split)

    seen = set()
    uniq = [x for x in l if x not in seen and not seen.add(x)]

    print(len(seen))
    print(len(uniq))

#test_proc()

def test_adding():
    l = []
    with (open(logfile, "r")) as f:
        lines = f.readlines()
        for line in lines:
            if 'adding' in line:
                split = line.split(' ')
                l.append(split[9].rstrip())

    for link in l:
        print(link)

    print(len(l))

    seen = set()
    uniq = [x for x in l if x not in seen and not seen.add(x)]

    print (len(seen))
    print (len(uniq))

    print(urlparse('https://www.cam.ac.uk/donate').netloc)


def testlink(link):
    with (open(logfile, "r")) as f:
        lines = f.readlines()
        for line in lines:
            if link in line:
                print(line)

#testlink('http://www.cam.ac.uk/research')
#d = LinkDownloader('http://www.cam.ac.uk/taxonomy/term/36022/feed')
#html = d._read_from_disc(d.url)
#e = LinkExtractor()
#print(e._find_links(html))

#req = Request('https://www.cam.ac.uk/robots.txt', headers={'User-Agent': 'Mozilla/5.0'})
#resp = urlopen(req, context=ssl._create_unverified_context())
#print(resp.read())
#
# from reppy.robots import Robots
# from bs4 import BeautifulSoup, SoupStrainer
#
# robots = Robots.fetch('https://www.cam.ac.uk/robots.txt')
#
# agent = robots.agent('*')
# allowed = agent.allowed('https://www.cam.ac.uk')
# if allowed:
#     req = Request('https://www.cam.ac.uk', headers={'User-Agent': 'Mozilla/6.0'})
#     data = urlopen(req, context=ssl._create_unverified_context()).read()
#     for link in BeautifulSoup(data, parseOnlyThese=SoupStrainer('a')):
#         if link.has_attr('href'):
#             print(link['href'])
#print (agent.delay)