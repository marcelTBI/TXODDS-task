from threading import Thread
import time
import random
import sys
from queue import Queue
from urllib import request
import re
import unittest

# maximum number of queue items
max_items = 10
to_do = Queue(max_items)

def fetch_url(line):
    # try to fetch the designated url:
    if len(line)==0:
        return None
    print("Try to fetch: ", line)
    try:
        opened_url = request.urlopen(line, timeout=2)
    except request.URLError as err:
        print("Error on fetching:", line, err, file=sys.stderr)
    except ValueError as err:
        print("Unknown url type, forgot \"http(s)://\"?", line, err, file=sys.stderr)
    else:
        return opened_url
    return None


class Producer(Thread):
    def run(self):
        global to_do
        print("Producer starts")
        # open the designated stream/file (in my case urls.txt)
        with open("urls.txt", "r") as file:
            for line in file:
                line = line.strip()
                opened_url = fetch_url(line)
                if opened_url:
                    to_do.put((line, opened_url))
                    print("Fetched:", line, file=sys.stdout)
                
        print("Producer stops")


def extract_hyperlinks(html):
    # hyperlinks regexp, can be done much more sophistically
    hlink_reg = re.compile("http://[^ >\"\'\\\\]+|https://[^ >\"\'\\\\]+")
    hlinks = hlink_reg.findall(html)
    return hlinks


class Consumer(Thread):
    
    stopping = False
    
    def stop(self):
        print("Consumer stops")
        self.stopping = True
    
    def run(self):
        print("Consumer starts")
        global to_do
        
        # delete contents of output file
        with open("output.txt", "w"): pass
        
        # consumer loop
        while not self.stopping:
            # fetch the webpage
            url_adress, opened_url = to_do.get()
            to_do.task_done()
            print("Crawling:", opened_url, file=sys.stdout)
            
            # parse the page:
            hyperlinks = extract_hyperlinks(str(opened_url.read()))
            
            # write them in the output:
            with open("output.txt", "a") as f_out:
                print("Opened: ", url_adress, "\nRedirected to:", opened_url.geturl().strip(), file=f_out)
                for i, hyper in enumerate(hyperlinks):
                    print(i+1, hyper, file=f_out)
                print("", file=f_out)   


Producer().start()
consumer = Consumer()
consumer.start()

time.sleep(5)

consumer.stop()


class Test(unittest.TestCase):
    def test_extract_hyoerlinks(self):
        hlinks = extract_hyperlinks("http://a.com <a \"https://b.com\"> ")
        self.assertEqual(len(hlinks), 2)
        self.assertEqual(hlinks[0], "http://a.com")
        self.assertEqual(hlinks[1], "https://b.com")
    def test_fetch_url(self):
        self.assertEqual(None, fetch_url(""))
        self.assertEqual(None, fetch_url("google.com"))
        # assume google is always available
        self.assertTrue(fetch_url("https://google.com")) 
        pass
    def test_Producer(self):
        pass
    def test_Consumer(self):
        pass
    
unittests = unittest.TestLoader().loadTestsFromTestCase(Test)
unittest.TextTestRunner(verbosity=2).run(unittests)

