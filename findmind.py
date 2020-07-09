import schedule
import time
from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl

def web_scrape():
    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    url = 'https://www.sebi.gov.in/sebiweb/home/HomeAction.do?doListing=yes&sid=3&s'
    html = urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, "html.parser")

    list_url=[]
    final_url_list=[]
    # Retrieve all of the anchor tags
    tags = soup('a')
    for tag in tags:
        # Look at the parts of a tag
        #print('TAG:', tag)
        #print('URL:', tag.get('href', None))
        redirect_url=tag.get('href',None)
        if redirect_url==None:
            continue
        if redirect_url.startswith('https://www.sebi.gov.in/filings/'):
            list_url.append(redirect_url)
    #print(list_url)
    for index_url in list_url:
        url = index_url
        try:
            html = urlopen(url, context=ctx).read()
        except:
            continue
        soup = BeautifulSoup(html, "html.parser")
        tags = soup('a')
        for tag in tags:
            required_url=tag.get('href', None)
            if required_url==None:
                continue
            if required_url.endswith('pdf'):
                required_url=required_url.strip()
                final_url_list.append(required_url)
    for i in final_url_list:
        print(i)

web_scrape()

'''schedule.every().day.at("23:00").do(web_scrape)
while 1:
    schedule.run_pending()
    time.sleep(1)'''
