## -*- coding: utf-8 -*-
import urllib2, socket
import Queue, time
import filter
from urlparse import urlparse
from urlparse import urljoin
from bs4 import BeautifulSoup
from google import search
import gzip
import os
import time


urlQueue = Queue.Queue()
maxDepth = 2
maxTimeOut = 3

# add a list of urls to the waiting queue
def addToQueue(lst):
    for elem in lst:
        urlQueue.put(elem)
        
# returns a webpage instance
def fetchPage(url):
    request = urllib2.Request(url, None, 
                              {'Referer': 'http://www.poly.edu'})
    request.add_header('poly.edu.cs6913',
                'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)')
    try:
        page = urllib2.urlopen(request, timeout=maxTimeOut)
        return page
    except urllib2.URLError as e:
        print type(e)
        print e
        print url
        return None
    except socket.timeout as e:
        print type(e)
        print e
        print url
        return None
    except Exception as e:
        print type(e)
        print e
        return None
        
# returns a list of urls parsed from the given page
def parsePage(page, curr_url):
    next_url = list()
    if not filter.allow_types(page):
        print "page mimetype is not allowed"
        return next_url
    
    try:
        soup = BeautifulSoup(page)
        
        for link in soup.find_all('a'):
            temp = link.get('href')
            temp = urllib2.quote(temp.split('#')[0].encode('utf8'), 
                                 safe = "%/:=&?~#+!$,;'@()*[]") if temp else ''
            
            if bool(urlparse(temp).netloc):
                if not bool(urlparse(temp).scheme):
                    temp = urljoin(curr_url, temp)
                if urlparse(temp).scheme != "http" and urlparse(temp).scheme != "https":
                    continue
                next_url.append(temp)
            else:
                if urlparse(temp).path == "None":
                    continue
                if bool(urlparse(temp).path):
                    if urljoin(curr_url, temp) != temp:
                        next_url.append(urljoin(curr_url, temp))
                else:
                    continue                      
        return next_url
    except Exception as e:
        print type(e)
        print e
        return next_url
        
    
def get_page(url):
    print "get_page(...) called"
    print "urL:",url
    try:
        resp = urllib2.urlopen(url)
        page_content = resp.read()
        return page_content
    except urllib2.URLError,e:
        print e
        return ""
    except urllib2.HTTPError,e:
        print e
        return ""
    except Exception as e:
        #print type(e)
        print e
        return ""
        
        
# sample code here        
searchKey = "music"
searchList = [(elem, 0) for elem in search(searchKey, 10)]
addToQueue(searchList)
timer_1 = time.time()
#links = crawl_start()

'''########################test#######################'''

#queueStillNeededToBeRetrieved = []
dictAlreadyTriedAndSuccess = {}
dictAlreadyTriedButFailed = {}
allWebPagesContent = []
total_links_counter = 0  #all links that have been crawled
succeedDownloadLinks = 0  #only count the number of links which succeeded download
totalFile = 0  # counter for file storage
        
while not urlQueue.empty():
    total_links_counter += 1
    start_time = time.time()
    curr_url, curr_dep = urlQueue.get()[0:2]
    print "Depth:%s  %s" % (curr_dep, curr_url)
    if filter.allow_robot(curr_url):
        # check the duplication
        if curr_url not in dictAlreadyTriedAndSuccess.keys() and \
            curr_url not in dictAlreadyTriedButFailed.keys() :  #no duplication
            page = fetchPage(curr_url)  #return the top 10 results form search engine
            allWebPagesContent.append(get_page(curr_url)) #download the page and store the content
            dictAlreadyTriedAndSuccess[curr_url] = "Succeed"
            succeedDownloadLinks += 1
        else:  #find a duplication
            continue
    else:
        print "robot is not allowed to crawl this url"
        page = None
        dictAlreadyTriedButFailed[curr_url] = "Failed"
        # log here
        # robot is not allowed to crawl this url
    if page and curr_dep <= maxDepth:
        rawList = [(elem, curr_dep+1) for elem in parsePage(page, curr_url)]
        addToQueue(rawList)
    else:
        print "no page is fetched or reach the maximum depth"           
        # log code here
        # no page is fetched or reach the maximum depth
    end_time = time.time() - start_time
    print end_time
    print "You've already crawled: %d." % total_links_counter
    
    #save the pages as a file to release the main memory
    if succeedDownloadLinks == 10:
        #print allWebPagesContent
        #print '\n'.join(str(i) for i in allWebPagesContent)
        
        #store allWebPagesContent to the hard drive as a gzip file
        ''' outputFileHandler = open("webPages.txt","w") 
        for i in allWebPagesContent:
            outputFileHandler.write(i + "\n")'''
        b = os.path.exists("/Users/apple/Documents/testfolder/")
        if b:
            print "Folder Exist!"
        else:
            os.mkdir("/Users/apple/Documents/testfolder/")
        
        filePostfix = totalFile
        fileName = "/Users/apple/Documents/testfolder/"+ "webpagetest" + str(filePostfix) +".txt.gz"
        f = gzip.open(fileName, "ab")
        for i in allWebPagesContent:
            f.write(i + "\n")
        f.close()
        '''outputFileHandler.close()'''
        print "File" + "" + str(filePostfix) + ":" + fileName
        time.sleep(1)
        print "done"
        totalFile += 1
        allWebPagesContent = []  #clear download pages in main memory
        succeedDownloadLinks = 0 #clear download counter for next 500 pages
        print "All done"
        #break

print "Total time: %s. Total links crawled: %s" % (time.time()-timer_1, total_links_counter)
'''########################test ends#######################'''

#addToQueue(search(searchKey, 10))
#try:
#    urlfile = open('url.txt', 'w')
#    while not urlQueue.empty():
#        start_time = time.time()
#        curr_url = urlQueue.get()
#        urlfile.write('\n#Parsing... '+curr_url)
#        urlfile.write('\n####################################\n')
#        page = fetchPage(curr_url)
#        if page:
#            for url in parsePage(page, curr_url):
#                #######################
##                pge = fetchPage(url)
##                if pge:
##                    print "%s  %s" % (pge.info()['Content-Type'].split(';')[0], url)
##                else:
##                    print "$$$$$$$$$$$" + curr_url
#                ########################
#                urlfile.write(str(url)+'\n')
#        print time.time()-start_time
#except IOError:
#    pass
#finally:
#    urlfile.close()
