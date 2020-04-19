import json
from bs4 import BeautifulSoup
import pandas as pd
from functions_for_scraper import zipcode_search, options_creator
import requests
from datetime import datetime


def scrape(old_houses_url):

    url = "https://www.woonnet.nl/huurwoning/amsterdam"

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    nr_of_pages = int(str(soup.find_all(class_= 'page-item d-none d-md-inline-block')[-1].contents)[-7:-5])

    house_dict = {}


    for page in range(1, nr_of_pages+1):
        print('pagina ', page)
        url = "https://www.woonnet.nl/huurwoning/amsterdam/page/{}".format(page)
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')

        houses_per_page = soup.find_all(class_='card position-relative mb-3 py-2 px-2')
        count = 0
        for house in houses_per_page:
            count = count + 1
            print('adv ', count)

            # Get objects of each house
            price = str(house.find_all(class_='mt-4 mt-md-3 mb-md-5')).split()[4].split('.')[0]
            try:
                price = float(price[1:])
            except ValueError:
                price = float(price[1:].split(',')[0])
            location = house.find(class_='col-8 col-md-6 pt-md-3 col-descriptionwidth-small').contents
            url = str(location[1]).split('"')[1]
            
            if url not in old_houses_url:
                
                street = (str(location[1]).split('"')[2])[1:-9]
                zipcode = str(location[3]).split()[2] + ' ' + str(location[3]).split()[3]
                
                if zipcode.startswith('Amsterdam'):
                    zipcode = zipcode_search(street)

                char = house.find(
                        class_='description pb-0 mb-0').contents
                
                try:
                    sq = int(str(char[2]).strip().split()[0])
                except:
                    sq = 999

                try:
                    rooms = int(str(char[4]).split()[0])
                except:
                    rooms = 99

                try: 
                    gestoffeerd = str(char[6].strip())
                except:
                    gestoffeerd = 'onbekend'

                try:
                    available = str(char[8]).strip().split()[-1]
                except:
                    available = 'onbekend'

                
                house_dict[url] = [street, zipcode, price, sq, rooms, gestoffeerd, available, str(datetime.today())]
        
    return house_dict


if __name__ == '__main__':
    
    old_houses = pd.read_csv('alle_huisjes.csv', index_col = 0)
    old_houses_url = set(old_houses.index.values)
    
    all_houses = scrape(old_houses_url)
    
    df_all = pd.DataFrame.from_dict(data = all_houses, orient='index', columns=['street', 'zipcode', 'price', 'sq', 'rooms', 'gestoffeerd', 'available', 'date added'])
    print(df_all)
    old_dates = ['01-04-2020' for _ in range(len(old_houses))]
    old_houses['date added'] = old_dates
    print(old_houses)
    
    total_houses = old_houses.append(df_all)
    print(total_houses)

    total_houses.to_csv('huizen_alle.csv')
    
