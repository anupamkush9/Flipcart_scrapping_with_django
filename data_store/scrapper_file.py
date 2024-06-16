from bs4 import BeautifulSoup
import time
from time import sleep
import requests
from celery import shared_task
from authentication.models import User
from .models import Datastore
import traceback

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
            print("Error in setsoup")
            print(traceback.format_exc())
            exit()

    def getdata(soup):
        try:
            title = soup.find('title') 
            
            if "503" in title.text:
                print(title.text)
                exit()
            time.sleep(3)
                
            for data in soup.findAll('div', class_="cPHDOP col-12-12"):
                product_name = data.findAll('div', attrs={'class' : 'KzDlHZ'})
                product_price = data.findAll('div', attrs={'class' : 'Nx9bqj _4b5DiR'})
                for names in product_name:
                    item_name.append(names.text)
                for price in product_price:
                    item_price.append(price.text)
                
                # time.sleep(2)
                try:
                    # # next_url = data.find('a', attrs={"class" : "_1LKTO3"}) #_1LKTO3
                    # nav = data.find('nav', class_="WSL9JP")
                    # # print(nav.prettify())
                    # next_url = nav.find('a', class_='cn++Ap')
                    # # breakpoint()
                    # if "Next" in next_url.find('span').text:
                    #     # breakpoint()
                    #     print(next_url['href'])
                    #     # breakpoint()
                    #     time.sleep(2)
                    #     getdata(setsoup(next_url['href']))   
                    
                    # else:
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
                except:
                    pass
        
        except Exception as e:
            print("Error in setsoup",e)
            print(traceback.format_exc())

    while 1:
        try:
            getdata(setsoup(base_url))
            break
        except Exception as e:
            print("Error in setsoup while calling",e)
            print(traceback.format_exc())
    data_store = Datastore.objects.filter(id=id).first()
    data_store.raw_data = stored_data
    data_store.status = "Completed"
    data_store.save()
    return None

    

    
    