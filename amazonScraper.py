# importing libraries

from selenium import webdriver

import bs4 as bs

import pandas as pd

import time
#--------------


searchQuery = 'Gaming Laptop' # Search Query

parentURL= 'https://www.amazon.in/' # getting a parent URL

url= 'https://www.amazon.in/s?k=' + searchQuery # creating a URL to make a search query

driver= webdriver.Chrome(r'D:\Chrome Driver\chromedriver.exe') #instantiating the browser using selenium

driver.get(url) 

content= driver.page_source

soup= bs.BeautifulSoup(content)

last_page= soup.find('span',{'class':'s-pagination-item s-pagination-disabled'}).text # Finding the last page
last_page= int(last_page)



productName= []
price= []
rating= []
current_page= 1

## while loop to go through all the pages
while current_page <= last_page:
    driver.get(url)
    content= driver.page_source
    soup= bs.BeautifulSoup(content)
    
    for each in soup.find_all(name= 'div', attrs= {'class':'a-section a-spacing-small a-spacing-top-small'}):
        try:
            rating_scraped = each.find('span',{'class':'a-icon-alt'}).text
            price_scraped = each.find('span',{'class':'a-price-whole'}).text
            productName_scraped = each.find('span',{'class':'a-size-medium a-color-base a-text-normal'}).text
        except:
            rating_scraped= '0.0' # Catching error where rating is unavailable

        
        productName.append(productName_scraped)
        price.append(price_scraped)
        rating.append(rating_scraped)
    try:    
        next_page_link = soup.find(name= 'a', attrs= {'class':'s-pagination-item s-pagination-next s-pagination-button s-pagination-separator'})['href']
    except:
        print('Last Page') # When pages go to the last page
    
    url = parentURL + next_page_link # Next page link
    
    current_page += 1 # counting pages
    
    time.sleep(20) # Delay to avoid getting banned
    
    
    
# cleaning up the data and adding it to a csvfile


    

df= pd.DataFrame({'Product Name':productName, 'Rating':rating, 'Price':price}) # creating a dataframe

df['Rating'] = df['Rating'].apply(lambda x : x.strip()) # cleaning up leading and trailing spaces

df= df[df['Rating'] != 'SponsoredSponsored'] # Removing all sponsored products

df['Rating'] = df['Rating'].apply(lambda x : float(x[:3])) # Changing rating values to floats

df['Price'] = df['Price'].apply(lambda x : x.replace(',','')) # removing commas from price values

df['Price'] = df['Price'].astype(float) #changing price values to floats

df.to_csv(f'{searchQuery}_amazon_search_non_sponsored.csv')


                  
