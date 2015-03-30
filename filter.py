from urlparse import urlparse
import robotparser

def allow_robot(url):
    parsed = urlparse(url)
    rbturl = "%s://%s/robots.txt" % (parsed.scheme, parsed.netloc)
    rp = robotparser.RobotFileParser()
    try:
        rp.set_url(rbturl)
        rp.read()
        return rp.can_fetch("poly.edu.cs6913", url)
    except Exception as e:
        print e
        print "allow_robot() error"
        return False

def allow_types(page):
    if page.info()['Content-Type'].split(';')[0] == 'text/html':
        return True
    else:
        return False
    
#just for test
#url = "http://www.nyu.edu/hr/pdf/forms/fmlasinf.pdf"   #"http://en.wikipedia.org/wiki/Main_Page"
#print allow_robot(url)