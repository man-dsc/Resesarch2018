# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 16:04:42 2018

@author: Summer16 ROSS BARTLETT

scrape apps made by each top developer on google play store 

-given csv of developer names
-output a csv for each dev, containing a list of their apps 

-have to scroll and click the 'show more' button for 
-devs with many apps

-outputs [appnames,applinks,packnames] to csv in dir 'developer_applists'

speed:
    -took ~1h40m for input of 780 devnames
"""
def search():
    import requests, bs4, csv, time, re, os, urllib2

    #from selenium import webdriver
    #from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException

    def powerset(s):
        print('a')
        r = [[]]
        for e in s:
            print('b')
            r += [x+[e] for x in r]
        return r
    print('c')

    def get_apps(html_source, num3, query):    
        print('d')
        soup = bs4.BeautifulSoup(html_source,'html.parser') 

        # return a list of tuples: (appname, link, packname)
        if num3 == 0:
            print('e')
            #tags = soup.findAll('a', class_='title', href=re.compile('^'))
            #return[(tag)]
            headers = {
            'User-Agent':'iTunes/10.3.1 (Macintosh; Intel Mac OS X 10.6.8) AppleWebKit/533.21.1',
            'Accept-Encoding' : 'identity'
            }
            endPoint = 'https://itunes.apple.com/search?term={}&media=software&retries=true&limit={}'.format(query, 30)
            result = requests.get(endPoint, headers=headers)
            print(result)
            try:
                print('f')
                apps = result.json()['results']
                #print(apps)
                print('g')
            except ValueError:
                print('errpor')
                
                return
            if apps:
                print('h')
                rowdata = []
                for pair in apps:
                    name = pair.get('trackName').replace('&nbsp;', '').encode("utf-8")
                    bundleId = pair.get('bundleId').replace('&nbsp;', '').encode("utf-8")
                    desc = pair.get('description').replace('&nbsp;', '').encode("utf-8")
                    rating = pair.get('averageUserRating')
                    ratingCount = pair.get('userRatingCount')
                    dev = pair.get('artistName').replace('&nbsp;', '').encode("utf-8")
                    rowdata.append([name, dev])
                return rowdata
        if num3 == 1:
            print('i')
            #get all the apps on the page 
            tags = soup.findAll('a', class_='title', href=re.compile('^/store/apps/details'))
            href_start = 'https://play.google.com'
            print(tags) 
            return [(tag['title'], href_start+tag['href'], tag['href'][tag['href'].rfind('=')+1:]) for tag in tags]
    
    print('j')
    
    def get_last_on_page(html_source):
        print('s')
        # return the appname of the last app on the page 
        # used to check if a dev has a small amount of apps
        # does not need to 'scroll to end'
        soup = bs4.BeautifulSoup(html_source,'html.parser') 
        tags = soup.findAll('a', class_='title', href=re.compile('^/store/apps/details'))
        return tags[-1]['title'] 
        

    def scroll_to_end(browser):
        # scrolls to the end of the page and hits the "show more" button 
        # have to experiment with the sleep time and for-loops to ensure it doesnt stop before all reviews found 
        # has a delay once the end of page is found before returning 
        count = 0
        tries = 0
        last1 = get_last_on_page(browser.page_source)
        while True:
            try:
                for i in range(3):
                    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);") # scroll to bottom
                    browser.execute_script("scrollBy(0,-300)") # scroll back up a little
                    time.sleep(1)
                last2 = get_last_on_page(browser.page_source)
                if last1 == last2:
                    # if all the dev's apps fit on one page
                    # this more than halves the runtime 
                    print('quick return')
                    return 0

                show_more_button = browser.find_element_by_id("show-more-button")
                show_more_button.click()    
                count += 1
                print("clicked 'show more' button:", count)
            except ElementNotInteractableException as e:
                #print('couldnt find button...', tries)
                if tries >=2 :
                    #print('done scrolling')
                    return count
                tries += 1
            except NoSuchElementException:
                # another type of url not found error on the google play store
                return -1



    def get_html_source(url):

        response = urllib2.urlopen(url.replace(' ', '+'))
        # scroll to end to ensure all reviews are exoosed on page 
        # clicks stores the num of times the 'show more' button was clicked
        #clicks = scroll_to_end(browser)
        #if clicks == -1:
        #    print('error with url:',url)
        #    return None
        # need to use Selenium to get the page, then pass the page_source to 
        # BeautifulSoup in order to search the html because
        # the webpage is rendered w/ javaScript, which beautifulSoup can't handle
        # on it's own 
        #print(clicks,'clicks')
        return response.read() 

    def read_query():
       global On

       with open('querys.csv', 'r') as qfile:
           reader = csv.reader(qfile)
           qry = []
           numb = 0
           for row in reader:
                if numb == 0:
                    On = row[0]
                    numb += 1
                else:
                    qry.append(row[0])
       return qry

    def print_results():
        pass
    '''
    def write_to_csv(devname):
        # write appnames,applinks to csv
        outdir = 'developer_applists'
        clean_name = devname.replace(' ','_').replace('/','_')
        outname = 'applist_'+clean_name+'.csv'
        outname = os.path.join(outdir, outname)
        success_count = 0
        invalid_apps = []
        with open(outname,'w', newline='', encoding='latin-1') as f:
            wr = csv.writer(f)
            for app in apps:
                try:
                    wr.writerow([app[0],app[1],app[2]]) #name,link,packname
                    success_count += 1
                except UnicodeEncodeError:
                    # still write names containing non latin-1 chars, but 
                    # keep track of them in invalid list 
                    #print('error outputting:', app[0])
                    cleaned_name = app[0].encode('latin-1', 'replace').decode('latin-1') # replaces non-latin-1 chars with '?'

                    wr.writerow([cleaned_name,app[1],app[2]]) #name,link,packname
                    invalid_apps.append(app)
                    continue

        if len(invalid_apps)>0:
            print(devname, 'apps with invalid names:',len(invalid_apps))

    '''


    # --------------------MAIN ----------------------
    start = time.time()


    #infile = 'cleaned_top_780_devnames.csv'

    #devnames = read_csv(infile)
    #print('devnames read from csv:',len(devnames))

    query = read_query()


    #browser = webdriver.Firefox()
    tot_apps = 0
    count = 0
    skipped = []
    qapps=[]
    apps2 = []
    num3 = 0
    urls = [('https://www.apple.com/ca/search/','?src=serp'), ('https://play.google.com/store/search?q=','&c=apps')]

    for ur in urls:
        for q in query:
            print('query:',q)
            count += 1
            if count%10==0:
                print('finsihed',count,'/',len(query))
                print('current time:', time.time()-start)

            url = (ur[0] + q + ur[1].replace(' ','+')).encode()
            html_source = get_html_source(url)
            if html_source == None:
                print(q, 'skipped')
                skipped.append(q)
                continue
            apps = get_apps(html_source, num3, q) # a list of tuples (appname,link,packname)
            print('sd')
            #print('found', len(apps), 'apps for query:',q)
            if apps is not None:
                
                tot_apps += len(apps)
            apps2.append(apps)
            #write_to_csv(devname)


        qapps.append([])
        for app in apps2:
            qapps[num3].append(app)
        #print(qapps)
        apps2 = []
        num3 += 1
    end = time.time()

    print('')
    print('')
    print('success:', count)
    print('skipped:', len(skipped))
    print('total apps;', tot_apps)
    print('')
    print('')
    print('done! time:',end-start, 'secs')

    stores = ['Apple App Store', 'Google Play Store']

    with open('appdata.csv', 'wb') as f2:
        writer = csv.writer(f2)
        num = 0
        num2 = 0
        print(len(qapps), len(stores))
        #print(qapps[1])
        #print(qapps[0])
        for apps in qapps:
            writer.writerow([stores[num]])
            print(On)
            if num == 0 and '1' in On:
                apps3 = apps[0]
                try:
                    if apps is not None:
                        for app in apps:
                            if app is not None:
                                print(app)
                                try:
                                    print(len(app), num)
                                except:
                                    print('exceptdsfa')
                                for ap in app:
                                    
                                    try:
                                        writer.writerow([ap[0], ap[1]])
                                    except:
                                        print([ap[0],ap[1]])
                except:
                    print('2 error')
            print("here")
            if num == 1 and '2' in On:
                try:
                    if apps is not None:
                        for app in apps:
                            #print(app)
                            for ap in app:
                                try:
                                    writer.writerow([ap[0].encode('utf8'), ap[2].encode('utf8')])
                                except:
                                    print('erooro')
                except:
                    print('3 error')
            num += 1
            #print(apps)
            '''for app in apps:
                if apps == qapps[1]:
                    writer.writerow([app[0].encode('utf8'), app[2].encode('utf8')])
                elif apps == qapps[0]:
                    writer.writerow([app[0][0],app[0][1]])
            '''

