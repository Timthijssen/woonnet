import requests
import json
from bs4 import BeautifulSoup
import pandas as pd

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
        # Get object of each house

        price = str(house.find_all(class_='mt-4 mt-md-3 mb-md-5')).split()[4]


        location = house.find(class_='col-8 col-md-6 pt-md-3 col-descriptionwidth-small').contents

        url = (str(location[1]).split('"')[1])
        street = (str(location[1]).split('"')[2])[1:-9]
        zipcode = str(location[3]).split()[2] + ' ' + str(location[3]).split()[3]
        char = house.find(
                class_='description pb-0 mb-0').contents
        
        
        sq = str(char[2]).strip()
        
        try:
            rooms = str(char[4]).split()[0]
        except TypeError:
            rooms = 'onbekend'

        try: 
            gestoffeerd = str(char[6].strip())
        except:
            gestoffeerd = 'onbekend'

        try:
            available = str(char[8]).strip().split()[-1]
        except:
            available = 'onbekend'
        house_dict[url] = [street, zipcode, price, sq, rooms, gestoffeerd, available]


df = pd.Dataframe(data = house_dict)
print(df)
print(house_dict)



# Select options from house_dict
zipcode_dict = json.loads(open('Postcode_damsco.txt', 'r').read())


options = {house[0]: house[1] for house in house_dict.items() 
               if house[1][1][:4] in zipcode_dict 
               and int(house[1][2][:-3]) >= 50 
               and int(house[1][3]) >= 2}


print(options)
