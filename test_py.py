# from selenium import webdriver
# from bs4 import BeautifulSoup
# from time import sleep


# #######################################
# #DRAFT FOR NOON AE

# #################################



# # star = []

# '''Open Selenium Driver Couse of flex'''
# driver = webdriver.Firefox()
# driver.get('https://www.noon.com/uae-en/iphone-13-pro-max-256gb-sierra-blue-5g-with-facetime-international-version/N50840187A/p/?o=c63a3dd3e009519d')
# sleep(3)
# driver.find_element_by_id('Reviews').click()
# sleep(3)
# html  = driver.page_source
# soup_en = BeautifulSoup(html,"html.parser")

# '''English Reviews'''
# rev_en = soup_en.find_all('div',class_='reviewDesc')
# date_en = soup_en.find_all('div',class_='ratedDate')
# star_en = soup_en.find_all('div',class_='ratingCover')
# for i in range(0,len(rev_en)) :
#     print(rev_en[i].get_text().strip())
#     print(date_en[i].get_text().strip())
#     # star.append(str(star_en[i]).count('oneStar'))
#     print(str(star_en[i]).count('oneStar'))

# '''Arabic Reviews if exists '''
# driver.find_element_by_css_selector('div.select_lang:nth-child(3)').click()
# html_ar = driver.page_source
# soup_ar = BeautifulSoup(html_ar,"html.parser")
# ## there is no diff between soup_en or ar here becouse of selenium
# rev_ar = soup_ar.find_all('div',class_='reviewDesc')
# date_ar = soup_en.find_all('div',class_='ratedDate')
# star_ar = soup_en.find_all('div',class_='ratingCover')
# try :
#     ### try catching arabic reviews if exists and appending them into data
#     for i in range(0,5) :
#         print(rev_ar[i].get_text().strip())
#         print(date_ar[i].get_text().strip())
#         # star.append(str(star_ar[i]).count('oneStar'))  <<<< this is the right way 
#         print(str(star_ar[i]).count('oneStar'))
# except :
    
#     print('There are no Arabic Reviews')



# from html.parser import HTMLParser
# from sys import unraisablehook
# import requests
# from bs4 import BeautifulSoup
# from selenium import webdriver
# import urllib
# url = 'https://www.amazon.eg/-/en/Realme-C25Y-6-5-inch-Mobile-Phone/dp/B09MJ9Y45R/ref=sr_1_1?keywords=mobile+phone&qid=1648291632&sprefix=mobi%2Caps%2C117&sr=8-1'
# page = urllib.request.urlopen(url).read()
# soup = BeautifulSoup(page,"html.parser")
# # print(soup.prettify())
# # img = soup.find_all('span',class_='a-button-text')
# # img = soup.find_all('span',class_='a-declarative')

# im = soup.find('img',class_='a-dynamic-image').get('src')
# print(im)

# # HEADERS = ({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64)AppleWebKit/537.36 (KHTML, like Gecko)Chrome/44.0.2403.157 Safari/537.36','Accept-Language': 'en-US, en;q=0.5'})
# # page = requests.get(url,headers=HEADERS)
# # html_contents = page.text
# # pro_soup = BeautifulSoup(html_contents,"html.parser")

# print(data)
# print(text)
# print(date)
# print(stars)

# file_name = os.path.join(general_path,title_path)
# Rev_list = []
# for i in range(0,len(text)): 
#     Rev_list.append(text[i])
#     Rev_list.append(date[i])
#     Rev_list.append(stars[i])
#     rev_file = open(file_name,'a',newline='')
#     rev_file_writer = csv.writer(rev_file)
#     rev_file_writer.writerow(Rev_list)
#     Rev_list.clear()
#     rev_file.close()

        # my_data = {
        # 'title' : pro_soup.find('span',class_='a-size-large product-title-word-break').get_text().strip(),
        # 'about_the_item' : pro_soup.find_all('span',class_='a-list-item')[-1].get_text().strip(),
        # 'brand' : pro_soup.find('tr',class_='a-spacing-small po-brand').find_all('span',class_='a-size-base')[1].get_text().strip(),
        # 'category' : pro_soup.find('ul',class_='a-unordered-list a-horizontal a-size-small').find_all('li')[-1].get_text().strip()
        # }

# FilePath = r"C:\Users\alaa_\OneDrive\Desktop\Product_Data.xlsx"
# with tarfile.open(FilePath, "r:gz") as gzip_file:
#     gzip_file.extractall()
# ExcelWorkbook = load_workbook(FilePath)
# writer = pd.ExcelWriter(FilePath, engine = 'openpyxl')
# # startrow = writer.sheets['sheet1'].max_row
# for sheetname in writer.sheets:
#     product_details_df.to_excel(writer,sheet_name=sheetname, startrow=writer.sheets[sheetname].max_row, index = False,header= False)
# # product_details_df.to_excel(writer, sheet_name = 'sheet1')
# # for i in writer.sheets :
# #     print(i)
# writer.save()
# writer.close()

# def to_excel_file (data,text,date,stars) :
#     pass

'''
some notes >>>>>
write try except 
def some functions to manage the data well
deal with the pages thing >> when we scrap we scrap just 10 reviews so we need to get them all
'''

# reviews = pro_soup.find_all('div',class_='a-expander-content reviewText review-text-content a-expander-partial-collapse-content')
# for i in reviews :
#     x= i.find('span',class_='cr-original-review-content').get_text()
#     if x == None :
#         continue
#     print(x)

'''--Search the needed Category--'''
# url = 'https://www.amazon.eg/s?k='+ search_item +'&language=en_AE'
# html = urllib.request.urlopen(url).read()
# soup = BeautifulSoup(html,"html.parser")
# ###############################
# '''Find the href of the first 10 tags'''
# tags = soup.find_all('a',class_='a-link-normal s-no-outline')
# # j = 1
# # while j < 10 :
# Link = tags[0].get('href',None)
# ##############################
# '''Request the product URL'''
# product_url = 'https://www.amazon.eg/'+ Link

# myfile = open('test.txt','a',encoding='utf-8')
# print ('sleeping')
# time.sleep(2)
##############################################
# myfile.write(review)
    # myfile.write("-------------")

# # time.sleep(2)
# # print('sleeping the loop')
#     # j+= 1

####### we neeed to ulter the code of about the product and finish appending in csv file 
#### thank you come again 

# print(data['title'])
# print(text)
# print(date)
# print(stars)
# data = []
# data.append(data_dic)
# product_details_df = pd.DataFrame(data=data,index=[0])
# product_details_df.append(datax,ignore_index=True)
# product_details_df['Title'] = data['title']
# product_details_df['About Item'] = data['about_the_item']
# product_details_df['Brand'] = data['brand']
# product_details_df['Category'] = data['category']
# field = ['title','about item','Brand','Category']
# print(product_details_df)
# lis = []
# lis.append(product_details_df)
# print(lis)

# print(data)

# general_path = r'C:\Users\alaa_\OneDrive\Desktop'