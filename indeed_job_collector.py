'''
Created on Jan 15, 2016

@author: timbo

This script will just use general queries from the API page, not my saved jobs.

Source for the API: http://www.indeed.com/jsp/htmlbox.jsp#opt2
More info on the contents of the query: https://ads.indeed.com/jobroll/xmlfeed

'''
import requests
from bs4 import BeautifulSoup
import time
import csv
from urllib.request import urlopen

publisher = '############' #user needs to enter their publisher ID here
query = 'data_science' #enter query as string here
zip_code = '20003' #enter desired zipcode as location
radius = '30' #enter desire radius or defualt will be 25 miles
job_type = '' #accepted values are 'fulltime', 'parttime', 'contract', 'internship', 'temporary'
limit = '1000' #enter desired number of responses here
start = 0

url = 'http://api.indeed.com/ads/apisearch?publisher={p}&q={q}&l={l}&sort=&radius={r}&st=&jt={jt}&start={starting_point}&limit={lim}&fromage=&filter=&latlong=1&co=us&chnl=&userip=1.2.3.4&useragent=Mozilla/%2F4.0%28Firefox%29&v=2'.format(p=publisher,q=query,l=zip_code,r=radius,jt=job_type,starting_point = start, lim=limit)

job_keys = []

def get_total(url):
    page = requests.get(url)
    result_soup = BeautifulSoup(page.content, 'html.parser')
    tr_base = result_soup.findAll('totalresults')
    total_result = tr_base[0].text
    
    return total_result

def get_keys():
    start = 0
    url = 'http://api.indeed.com/ads/apisearch?publisher=9680490371724938&q={q}&l={l}&sort=&radius={r}&st=&jt={jt}&start={starting_point}&limit={lim}&fromage=&filter=&latlong=1&co=us&chnl=&userip=1.2.3.4&useragent=Mozilla/%2F4.0%28Firefox%29&v=2'.format(q=query,l=zip_code,r=radius,jt=job_type,starting_point = start, lim=limit)
    while start < int(get_total(url)):
        page = requests.get(url)
        result_soup = BeautifulSoup(page.content, 'html.parser')
        key_base = result_soup.findAll('jobkey')
        start += 25
        url = 'http://api.indeed.com/ads/apisearch?publisher=9680490371724938&q={q}&l={l}&sort=&radius={r}&st=&jt={jt}&start={starting_point}&limit={lim}&fromage=&filter=&latlong=1&co=us&chnl=&userip=1.2.3.4&useragent=Mozilla/%2F4.0%28Firefox%29&v=2'.format(q=query,l=zip_code,r=radius,jt=job_type,starting_point = start, lim=limit)

        #print(start)
        #print(url)    #I included these lines to verify that the script was updating the start and URL as intended
        
        for jk in key_base:
            job_keys.append(jk.text)
    
        time.sleep(2)  

def copy_keys():
    open('jobkeys-{q}-{l}.csv'.format(q=query,l=zip_code), 'w').close()
    with open('jobkeys-{q}-{l}.csv'.format(q=query,l=zip_code), 'w') as f:
        for item in job_keys:
            jkwriter = csv.writer(f)    
            jkwriter.writerow([item])

def copy_text():
    open('jobtext-{q}-{l}.txt'.format(q=query,l=zip_code), 'w').close()
    with open('jobtext-{q}-{l}.txt'.format(q=query,l=zip_code), 'a+b') as jobfile:
        for item in job_keys:
            newurl = 'http://www.indeed.com/viewjob?jk='+item
            html = urlopen(newurl)
            ind_soup = BeautifulSoup(html, 'html.parser')
            job_spans = ind_soup.findAll('span','summary')
            for span in job_spans:
                count=1
                words = span.text
                encodedwords = words.encode('ascii','replace')
                try:
                    jobfile.write(encodedwords)
                    count+=1
                except UnicodeEncodeError as detail:
                    print('Could not write.', detail)
                    count+=1
                    continue

get_keys()
copy_keys()
copy_text()
