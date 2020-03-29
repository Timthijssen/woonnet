import requests
import json
from bs4 import BeautifulSoup

url = "https://www.woonnet.nl/huurwoning/amsterdam"

page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
houses_per_page = soup.find_all(class_='card position-relative mb-3 py-2 px-2')

house_dict = {}

for house in houses_per_page:

    # Get object of each house
    location = house.find(class_='col-8 col-md-6 pt-md-3 col-descriptionwidth-small').contents

    url = (str(location[1]).split('"')[1])
    street = (str(location[1]).split('"')[2])[1:-9]
    zipcode = str(location[3]).split()[2] + ' ' + str(location[3]).split()[3]
    char = house.find(
            class_='description pb-0 mb-0').contents
    sq = str(char[2]).strip()
    
    rooms = str(char[4]).split()[0]
    gestoffeerd = str(char[6].strip())
    available = str(char[8]).strip().split()[-1]

    #print(url, street, zipcode, sq, rooms, gestoffeerd, available, zipcode)
    house_dict[url] = [street, zipcode, sq, rooms, gestoffeerd, available]

print(house_dict)



# Select options from house_dict
zipcode_dict = json.loads(open('Postcode_damsco.txt', 'r').read())


options = {house[0]: house[1] for house in house_dict.items() 
               if house[1][1][:4] in zipcode_dict 
               and int(house[1][2][:-3]) >= 50 
               and int(house[1][3]) >= 2}


print(options)
