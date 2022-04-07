import urllib.request ,urllib.parse,urllib.error
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
import csv
from selenium import webdriver
from time import sleep


def amazoneg(url,noonurl) :
    try :
        '''Requesting '''
        
        pro_req = urllib.request.urlopen(url).read()
        pro_soup = BeautifulSoup(pro_req,"html.parser")
        site = urllib.request.urlopen(noonurl).read()
        soup = BeautifulSoup(site,"html.parser")
        time.sleep(2)
        my_data = []
        mylis= []
        title =  pro_soup.find('span',class_='a-size-large product-title-word-break').get_text().strip()
        # about_the_item = pro_soup.find_all('span',class_='a-list-item')[-1].get_text().strip()
        brand = pro_soup.find('tr',class_='a-spacing-small po-brand').find_all('span',class_='a-size-base')[1].get_text().strip()
        category =  pro_soup.find('ul',class_='a-unordered-list a-horizontal a-size-small').find_all('li')[-1].get_text().strip()
        img = pro_soup.find('img',class_='a-dynamic-image').get('src')
        overview = soup.find('div',class_='sc-b21e051a-4 eVemVg').find_all('li')
        for i in overview :
            mylis.append(i.get_text())
        overview_text = '.'.join(mylis)
        my_data.append(title)
        my_data.append(brand)
        my_data.append(category)
        my_data.append(img)
        my_data.append(overview_text)
        # my_data.append(about_the_item)
        '''Finding the a Tag of All Reviews'''
        all_reviews = pro_soup.find('a',class_='a-link-emphasis a-text-bold')
        
        '''Requesting the All Reviews URl of the Product'''
        all_rev_link = 'https://www.amazon.eg/'+ all_reviews.get('href',None)
        req = urllib.request.urlopen(all_rev_link).read()
        all_rev_soup = BeautifulSoup(req,'html.parser')
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
            review_date.append(dt.get_text().replace('Reviewed in Egypt on ',''))
        stars = all_rev_soup.find_all('span',class_='a-icon-alt')
        for star in stars :
            
            review_stars.append(float(star.get_text().split(' ')[0]))
    except :
        print('There is no Reviews for this Product')
    return my_data , review_text, review_date ,review_stars

####################################
'''Saves the product data and creates excel sheet with amazon reviews'''
def saving_data(data,text,date,stars):
    try :
        '''putting the product details in csv file'''
        f = open(r'C:\Users\alaa_\Product_Data.csv','a',newline='')
        writer = csv.writer(f)
        # header = ['Title','Brand','Category','Img','Description']
        # writer.writerow(header)
        writer.writerow(data)
        f.close()
        '''putting the product reviews in seperate excel file'''
        title_path = data[0]+'.xlsx'
        Rev_list = []
        for i in range(0,len(text)) :
            dic ={
                'Review' : text[i],
                'Date' : date[i],
                'Stars' : stars[i]
            }
            Rev_list.append(dic)
        # if len(Rev_list) > 3 :
        df = pd.DataFrame(Rev_list)
        df.to_excel(title_path,index=False)
        return print('added successfully')
        # else :
        #     return print('there is no enough data')
    except :
        print('there isnot enough data ')


def Noon_ae(url):
    try :  
        star = []
        date = []
        rev  = []
        ''' Reviews & Dates and Stars '''
        ##Open Selenium Driver Couse of flex
        driver = webdriver.Firefox()
        driver.get(url)
        sleep(3)
        driver.find_element_by_id('Reviews').click()
        sleep(3)
        html  = driver.page_source
        soup_en = BeautifulSoup(html,"html.parser")

        '''English Reviews'''
        rev_en = soup_en.find_all('div',class_='reviewDesc')
        date_en = soup_en.find_all('div',class_='ratedDate')
        star_en = soup_en.find_all('div',class_='ratingCover')
        for i in range(0,len(rev_en)) :
            rev.append(rev_en[i].get_text().strip())
            date.append(date_en[i].get_text().strip())
            # star.append(str(star_en[i]).count('oneStar'))
            star.append(str(star_en[i]).count('oneStar'))
        
        '''Arabic Reviews if exists '''
        driver.find_element_by_css_selector('div.select_lang:nth-child(3)').click()
        html_ar = driver.page_source
        soup_ar = BeautifulSoup(html_ar,"html.parser")
        ## there is no diff between soup_en or ar here becouse of selenium
        rev_ar = soup_ar.find_all('div',class_='reviewDesc')
        date_ar = soup_ar.find_all('div',class_='ratedDate')
        star_ar = soup_ar.find_all('div',class_='ratingCover')
        try :
            ## try catching arabic reviews if exists and appending them into data
            for i in range(0,5) :
                rev.append(rev_ar[i].get_text().strip().replace('\n',' '))
                date.append(date_ar[i].get_text().strip())
                # star.append(str(star_ar[i]).count('oneStar'))  <<<< this is the right way 
                star.append(str(star_ar[i]).count('oneStar'))
                driver.close()
        except :
            print('There are no Arabic Reviews')
    except:
        print('There is no enough Reviews')
    return rev,date,star

#############################################

def Adding_data(data,text,date,stars):
    try :
        '''putting the product reviews in seperate excel file'''
        title_path = data[0]+'.xlsx'
        Rev_list = []
        for i in range(0,len(text)) :
            dic ={
                'Review' : text[i],
                'Date' : date[i],
                'Stars' : stars[i]
            }
            Rev_list.append(dic)
        df = pd.DataFrame(Rev_list)
        with pd.ExcelWriter(title_path, mode="a", engine="openpyxl",if_sheet_exists='new') as writer:
            df.to_excel(writer,index=False,sheet_name="Sheet2") 
        return print('Data Was appended')
    except :
        print('there isnot enough data ')

############################################
def amazonuk(url) :
    try :
            
        '''Requesting '''
        HEADERS = ({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64)AppleWebKit/537.36 (KHTML, like Gecko)Chrome/44.0.2403.157 Safari/537.36','Accept-Language': 'en-US, en;q=0.5'})
        page = requests.get(url,headers=HEADERS)

        html_contents = page.text
        pro_soup = BeautifulSoup(html_contents,"html.parser")
        time.sleep(2)
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
    return  review_text, review_date ,review_stars

def Adding_data2(data,text,date,stars):
    try :
        '''putting the product reviews in seperate excel file'''
        title_path = data[0]+'.xlsx'
        Rev_list = []
        for i in range(0,len(text)) :
            dic ={
                'Review' : text[i],
                'Date' : date[i],
                'Stars' : stars[i]
            }
            Rev_list.append(dic)
        df = pd.DataFrame(Rev_list)
        with pd.ExcelWriter(title_path, mode="a", engine="openpyxl",if_sheet_exists='new') as writer:
            df.to_excel(writer,index=False,sheet_name="Sheet3") 
        return print('Data Was appended again')
    except :
        print('there isnot enough data ')


noonurl ='https://www.noon.com/uae-en/airpods-with-wireless-charging-case-white/N22732307A/p/?o=a4afecac200fc90f'

url ='https://www.amazon.eg/-/en/Apple-Magic-Mouse-White-MLA02/dp/B00L6SHDLE/ref=sr_1_75?crid=AQIQLPWYR60M&keywords=apple&qid=1648550413&sprefix=appl%2Caps%2C154&sr=8-75'

ukurl ='https://www.amazon.co.uk/Apple-Airpods-Charging-latest-Model/dp/B07PZR3PVB/ref=sr_1_1?crid=3HODQWLBWCNGX&keywords=AirPods&qid=1648545789&sprefix=airpods%2Caps%2C178&sr=8-1'

'''calling amazon eg'''
data,text,date,stars = amazoneg(url,noonurl)
saving_data(data,text,date,stars)

# '''calling noon'''
# ntext,ndate,nstars=Noon_ae(noonurl)
# Adding_data(data,ntext,ndate,nstars)

# '''calling amazon uk'''
# utext,udate,ustars = amazonuk(ukurl)
# Adding_data2(data,utext,udate,ustars)


