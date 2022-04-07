import urllib.request ,urllib.parse,urllib.error
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import pandas as pd
#########################
mylis = []
my_data = []
star = []
date = []
rev  = []
def Noon_ae(url):
    try :
        ''' Product Data '''
        site = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(site,"html.parser")

        my_data.append(soup.find('h1',class_='sc-ebb3cc52-12 kVfnLm').get_text().strip())
        my_data.append(soup.find('div',class_='sc-ebb3cc52-11 heIyqT').get_text().strip())
        my_data.append(soup.find_all('div',class_='sc-f019e14d-2 ekDKTS')[-1].get_text().strip())
        overview = soup.find('div',class_='sc-b21e051a-4 eVemVg').find_all('li')
        for i in overview :
            mylis.append(i.get_text())
        overview_text = '.'.join(mylis)
        my_data.append(overview_text)
        # print(my_data[0])
        #########################################
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
        except :
            print('There are no Arabic Reviews')
    except:
        print('There is no enough Reviews')
    return my_data,rev,date,star

url = 'https://www.noon.com/uae-en/galaxy-a12-dual-sim-black-4gb-ram-128gb-4g-lte-middle-east-version/N43692696A/p/?o=ac3dc2d282968ccf'
data,rev,date,star = Noon_ae(url)
# saving_data(data,rev,date,star)

def Adding_data(data,text,date,stars):
    try :
        '''putting the product details in csv file'''
        
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
        # df.to_excel(title_path,index=False)
        with pd.ExcelWriter(title_path) as writer:
            df.to_excel(writer) 
        return print('scraping Adding')
        # else :
        #     return print('there is no enough data')
    except :
        print('there isnot enough data ')