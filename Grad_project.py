import csv
import urllib.request ,urllib.parse,urllib.error
import requests
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep

class Scaraping_data : 
    def AmazonEg( url, noonurl) :
        '''
        This fuction Scrapes Data
        from amazon egypt  

        It Scrapes Product Following Data 
        [title, brand, category, img, overview]

        Scarpes Reviews Data
        [Review text, Review Stars, Review Date]
        
        '''
        try :
            my_data = []
            my_lis = []
            review_text = []
            review_stars = []
            review_date = []


            #Requesting
            pro_req = urllib.request.urlopen(url).read()
            pro_soup = BeautifulSoup(pro_req,"html.parser")
            site = urllib.request.urlopen(noonurl).read()
            soup = BeautifulSoup(site,"html.parser")
            time.sleep(2)

            
            #Finding Tags
            title = pro_soup.find('span',class_='a-size-large product-title-word-break').get_text().strip()
            brand = pro_soup.find('tr',class_='a-spacing-small po-brand').find_all('span',class_='a-size-base')[1].get_text().strip()
            category = pro_soup.find('ul',class_='a-unordered-list a-horizontal a-size-small').find_all('li')[-1].get_text().strip()
            img = pro_soup.find('img',class_='a-dynamic-image').get('src')
            overview = soup.find('div',class_='sc-b21e051a-4 eVemVg').find_all('li')

            #Appending
            for i in overview : my_lis.append(i.get_text())    
            overview_text = '.'.join(my_lis)
            my_data.append(title)
            my_data.append(brand)
            my_data.append(category)
            my_data.append(img)
            my_data.append(overview_text)
            

            #Finding & Requesting the a Tag of All Reviews
            all_reviews = pro_soup.find('a',class_='a-link-emphasis a-text-bold')
            all_rev_link = 'https://www.amazon.eg/'+ all_reviews.get('href',None)
            req = urllib.request.urlopen(all_rev_link).read()
            all_rev_soup = BeautifulSoup(req,'html.parser')
            
            
            #Scraping The Data About The Product
            reviews = all_rev_soup.find_all('span',class_='a-size-base review-text review-text-content')
            dates = all_rev_soup.find_all('span',{'data-hook':'review-date'})
            stars = all_rev_soup.find_all('span',class_='a-icon-alt')
            
            #Appending
            for rev in reviews :
                review_text.append(rev.find('span').get_text().strip())
            
            for dt in dates :
                review_date.append(dt.get_text().replace('Reviewed in Egypt on ',''))
            
            for star in stars :    
                review_stars.append(float(star.get_text().split(' ')[0]))
            

        except :
            print('There is no Reviews for this Product')

        return my_data, review_text, review_date, review_stars



    def NoonAE(url):
        '''
        This fuction Scrapes Data
        from Noon UAE

        Scarpes Reviews Data
        [Review text, Review Stars, Review Date]
        
        '''
        try :  
            STAR = []
            DATE = []
            REV  = []


            #Open Selenium Driver Couse of flex
            ##Requesting
            driver = webdriver.Firefox()
            driver.get(url)
            sleep(3)
            driver.find_element_by_id('Reviews').click()
            sleep(3)
            html  = driver.page_source
            soup_en = BeautifulSoup(html,"html.parser")


            #English Reviews
            ## Finding
            rev_en = soup_en.find_all('div',class_='reviewDesc')
            date_en = soup_en.find_all('div',class_='ratedDate')
            star_en = soup_en.find_all('div',class_='ratingCover')
            
            
            #Appending
            for i in range(0,len(rev_en)) :
                REV.append(rev_en[i].get_text().strip())
                DATE.append(date_en[i].get_text().strip())
                STAR.append(str(star_en[i]).count('oneStar'))
            

            #Arabic Reviews if exists 
            ## Requesting
            driver.find_element_by_css_selector('div.select_lang:nth-child(3)').click()
            html_ar = driver.page_source
            soup_ar = BeautifulSoup(html_ar,"html.parser")


            #there is no diff between soup_en or ar here becouse of selenium
            ##Finding
            rev_ar = soup_ar.find_all('div',class_='reviewDesc')
            date_ar = soup_ar.find_all('div',class_='ratedDate')
            star_ar = soup_ar.find_all('div',class_='ratingCover')
            driver.close()


            #Appending
            try :
                #try catching arabic reviews if exists and appending them into data
                for i in range(0,5) :
                    REV.append(rev_ar[i].get_text().strip().replace('\n',' '))
                    DATE.append(date_ar[i].get_text().strip())
                    STAR.append(str(star_ar[i]).count('oneStar'))
        
            except :
                print('There are no Arabic Reviews')

        except:
            print('There is no enough Reviews')

        return REV,DATE,STAR


    def AmazonUK(url) :
        '''

        This fuction Scrapes Data
        from Amazon UK 

        Scarpes Reviews Data
        [Review text, Review Stars, Review Date]
        
        '''
        try :
            review_text = []
            review_stars = []
            review_date = []

            
            #Requesting 
            HEADERS = ({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64)AppleWebKit/537.36 (KHTML, like Gecko)Chrome/44.0.2403.157 Safari/537.36','Accept-Language': 'en-US, en;q=0.5'})
            page = requests.get(url,headers=HEADERS)
            html_contents = page.text
            pro_soup = BeautifulSoup(html_contents,"html.parser")
            time.sleep(2)

            
            #Finding
            all_reviews = pro_soup.find('a',class_='a-link-emphasis a-text-bold')


            #Requesting the All Reviews URl of the Product
            all_rev_link = 'https://www.amazon.co.uk/'+ all_reviews.get('href',None)
            req = requests.get(all_rev_link,headers=HEADERS)
            html_req = req.text
            all_rev_soup = BeautifulSoup(html_req,'html.parser')
            

            #Finding The Data About The Product
            reviews = all_rev_soup.find_all('span',class_='a-size-base review-text review-text-content')
            dates = all_rev_soup.find_all('span',{'data-hook':'review-date'})
            stars = all_rev_soup.find_all('span',class_='a-icon-alt')
            

            #Appending
            for rev in reviews :
                review_text.append(rev.find('span').get_text().strip())
            
            for dt in dates :
                review_date.append(dt.get_text().replace('Reviewed in Egypt on ',''))
            
            for star in stars :    
                review_stars.append(float(star.get_text().split(' ')[0]))
            

        except :
            print('There is no Reviews for this Product')

        return  review_text, review_date ,review_stars



    def SavingData(data, text, date, stars):
        '''
        Saves the product data & 
        Creates excel sheet with amazon reviews
        
        '''
        try :
            Rev_list = []


            #putting the product details in csv file
            csv_file = open(r'C:\Users\alaa_\Product_Data.csv','a',newline='')
            writer = csv.writer(csv_file)
            # header = ['Title','Brand','Category','Img','Description']
            # writer.writerow(header)
            writer.writerow(data)
            csv_file.close()


            #putting the product reviews in seperate excel file
            title_path = data[0]+'.xlsx'
            for i in range(0,len(text)) :
                dic = {
                    'Review' : text[i],
                    'Date' : date[i],
                    'Stars' : stars[i]}
                Rev_list.append(dic)
            df = pd.DataFrame(Rev_list)
            df.to_excel(title_path,index=False)

            return print('added successfully')
            
        except :
            print('there isnot enough data ')



    def AddingData(data,text,date,stars):
        '''

        Adding Reviews to a
        Seperate Excel Sheet
        
        '''
        try :
            rev_list = []
            #putting the product reviews in seperate excel file
            title_path = data[0]+'.xlsx'
            for i in range(0,len(text)) :
                dic ={
                    'Review' : text[i],
                    'Date' : date[i],
                    'Stars' : stars[i]}

                rev_list.append(dic)
            df = pd.DataFrame(rev_list)

            #Excel writing into new sheet 
            with pd.ExcelWriter(title_path, mode="a", engine="openpyxl",if_sheet_exists='new') as writer:
                df.to_excel(writer, index=False, sheet_name="Sheet2") 


            return print('Data Was appended')

        except :
            print('there isnot enough data ')

def AddingData_sh3(data,text,date,stars):
        '''

        Adding Reviews to a
        Seperate Excel Sheet
        
        '''
        try :
            rev_list = []
            #putting the product reviews in seperate excel file
            title_path = data[0]+'.xlsx'
            for i in range(0,len(text)) :
                dic ={
                    'Review' : text[i],
                    'Date' : date[i],
                    'Stars' : stars[i]}

                rev_list.append(dic)
            df = pd.DataFrame(rev_list)

            #Excel writing into new sheet 
            with pd.ExcelWriter(title_path, mode="a", engine="openpyxl",if_sheet_exists='new') as writer:
                df.to_excel(writer, index=False, sheet_name="Sheet3") 


            return print('Data Was appended')

        except :
            print('there isnot enough data ')






noonurl ='https://www.noon.com/uae-en/airpods-with-wireless-charging-case-white/N22732307A/p/?o=a4afecac200fc90f'

url ='https://www.amazon.eg/-/en/Apple-Magic-Mouse-White-MLA02/dp/B00L6SHDLE/ref=sr_1_75?crid=AQIQLPWYR60M&keywords=apple&qid=1648550413&sprefix=appl%2Caps%2C154&sr=8-75'

ukurl ='https://www.amazon.co.uk/Apple-Airpods-Charging-latest-Model/dp/B07PZR3PVB/ref=sr_1_1?crid=3HODQWLBWCNGX&keywords=AirPods&qid=1648545789&sprefix=airpods%2Caps%2C178&sr=8-1'

#calling amazon eg
# data,text,date,stars = Scaraping_data.AmazonEg(url,noonurl)
# Scaraping_data.SavingData(data,text,date,stars)

#calling noon
# ntext,ndate,nstars=Scaraping_data.NoonAE(noonurl)
# Scaraping_data.AddingData(data,ntext,ndate,nstars)

#calling amazon uk
# utext,udate,ustars = Scaraping_data.AmazonUK(ukurl)
# AddingData_sh3(data,utext,udate,ustars)
