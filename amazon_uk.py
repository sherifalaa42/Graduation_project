import urllib.request ,urllib.parse,urllib.error
from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv
import time
from Grad_project import saving_data



def amazonuk(url) :
    try :
            
        '''Requesting '''
        HEADERS = ({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64)AppleWebKit/537.36 (KHTML, like Gecko)Chrome/44.0.2403.157 Safari/537.36','Accept-Language': 'en-US, en;q=0.5'})
        page = requests.get(url,headers=HEADERS)

        html_contents = page.text
        pro_soup = BeautifulSoup(html_contents,"html.parser")
        # pro_req = urllib.request.urlopen(url).read()
        # pro_soup = BeautifulSoup(pro_req,"html.parser")
        time.sleep(2)
        my_data = []

        title =  pro_soup.find('span',class_='a-size-large product-title-word-break').get_text().strip()
        # about_the_item = pro_soup.find_all('span',class_='a-list-item')[-1].get_text().strip()
        brand = pro_soup.find('tr',class_='a-spacing-small po-brand').find_all('span',class_='a-size-base')[1].get_text().strip()
        category =  pro_soup.find('ul',class_='a-unordered-list a-horizontal a-size-small').find_all('li')[-1].get_text().strip()
        my_data.append(title)
        # my_data.append(about_the_item)
        my_data.append(brand)
        my_data.append(category)
        '''Finding the a Tag of All Reviews'''
        all_reviews = pro_soup.find('a',class_='a-link-emphasis a-text-bold')

        '''Requesting the All Reviews URl of the Product'''
        all_rev_link = 'https://www.amazon.co.uk/'+ all_reviews.get('href',None)
        req = requests.get(all_rev_link,headers=HEADERS)
        html_req = req.text
        all_rev_soup = BeautifulSoup(html_req,'html.parser')
        '''initiating lists to put the Data in '''
        review_text = []
        review_stars = []
        review_date = []

        '''Scraping The Data About The Product'''
        reviews = all_rev_soup.find_all('span',class_='a-size-base review-text review-text-content')
        for rev in reviews :
            # review = rev.find('span').get_text().strip()
            review_text.append(rev.find('span').get_text().strip())
        dates = all_rev_soup.find_all('span',{'data-hook':'review-date'})
        for dt in dates :
            # date = dt.get_text().replace('Reviewed in Egypt on ','')
            review_date.append(dt.get_text().replace('Reviewed in the United Kingdom on ',''))
        stars = all_rev_soup.find_all('span',class_='a-icon-alt')
        for star in stars :
            
            review_stars.append(float(star.get_text().split(' ')[0]))
    except :
        print('There is no Reviews for this Product')
    return my_data , review_text, review_date ,review_stars


url ='https://www.amazon.co.uk/Samsung-Galaxy-A12-Blue-Version/dp/B097QCY6F8/ref=sr_1_3?crid=22MISJ1GNDX0L&keywords=samsung+a12&qid=1647774803&sprefix=samsung+%2Caps%2C1039&sr=8-3'
data,text,date,stars = amazonuk(url)
saving_data(data,text,date,stars)

