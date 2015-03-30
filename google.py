import urllib2,urllib
import simplejson

# max results per page
resultPerPage = 8

# this function returns a list of urls fetched from www.google.com
# query = search keyword, num = number of results

def search(query, num):
    # number of pages should be fetched
    if num % resultPerPage > 0:
        maxPage = num / resultPerPage + 1
    else:
        maxPage = num / resultPerPage
    
    # fetch search results from google api page by page
    urllist = list()
    for i in range(maxPage):
        # start entry of the first result of current page
        start = i * resultPerPage
        
        # encode search keyword to be recognizable by program
        url = ('https://ajax.googleapis.com/ajax/services/search/web'
                  '?v=1.0&q=%s&rsz=%s&start=%s') % (urllib.quote(query), 
                                                    resultPerPage, start)
        try:
            # send search request, specify homepage of this app
            request = urllib2.Request(
            url, None, {'Referer': 'http://www.poly.edu'})
            response = urllib2.urlopen(request)
        
            # receive JSON object for search results
            # format standard at https://developers.google.com/web-search/docs/
            results = simplejson.load(response)['responseData']['results']
        except Exception as e:
            print e
        else:
            # last page should have less results
            if i == maxPage - 1 and num % resultPerPage != 0:
                for j in range(num % resultPerPage):
                    urllist.append(results[j]['url'])
                break
            # for other pages, append the whole page
            for res in results:
                urllist.append(res['url'])
                
    return urllist

