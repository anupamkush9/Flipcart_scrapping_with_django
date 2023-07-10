from bs4 import BeautifulSoup
import time
from time import sleep
import requests
from celery import shared_task
from authentication.models import User
from .models import Datastore
@shared_task
def scrapper(seach_key, id):
    print(seach_key, id)
    seach_key = seach_key.replace(" ","+")
    base_url = f"https://www.flipkart.com/search?q={seach_key}&"

    item_name = []
    item_price = []
    stored_data = []


    def setsoup(url):
        try:
            request = requests.get(base_url+url)
            soup = BeautifulSoup(request.content, "html.parser")
            return soup
        except Exception as e:
            print(e)
            exit()

    def getdata(soup):
        
        title = soup.find('title') 
        
        if "503" in title.text:
            print(title.text)
            exit()
        time.sleep(3)
            
        for data in soup.findAll('div', class_="_1YokD2 _3Mn1Gg"):
            product_name = data.findAll('div', attrs={'class' : '_4rR01T'})
            product_price = data.findAll('div', attrs={'class' : '_30jeq3 _1_WHN1'})
            for names in product_name:
                item_name.append(names.text)
            time.sleep(2)
            for price in product_price:
                item_price.append(price.text)
            
            time.sleep(2)
            # next_url = data.find('a', attrs={"class" : "_1LKTO3"}) #_1LKTO3
            nav = data.find('nav', class_="yFHi8N")
            # print(nav.prettify())
            next_url = nav.find('a', class_='_1LKTO3')
            # breakpoint()
            if "Next" in next_url.find('span').text:
                # breakpoint()
                print(next_url['href'])
                # breakpoint()
                time.sleep(2)
                getdata(setsoup(next_url['href']))   
            
            else:
                # print("Data Extracted Succesfully")
                
                for names in item_name:
                    received_data={}
                    received_data["name"] = names
                    for prices in item_price:
                        received_data["price"] = prices
                        item_price.remove(prices)
                        stored_data.append(received_data)
                        break
                print("=========", stored_data)
      
                # return stored_data
    while 1:
        
        getdata(setsoup(base_url))
        break
    data_store = Datastore.objects.filter(id=id).first()
    data_store.raw_data = stored_data
    data_store.status = "Completed"
    data_store.save()
    return None

    

    
    