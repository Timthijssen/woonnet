import requests
from bs4 import BeautifulSoup

url = "https://www.woonnet.nl/huurwoning/amsterdam"

page = requests.get(url)

soup = BeautifulSoup(page.text, 'html.parser')

houses_per_page = soup.find_all(class_='card position-relative mb-3 py-2 px-2')

for house in houses_per_page:
    rooms = house.find(
                class_='fas fa-bed')
        #class_='fas fa-bed')
    zipcode = house.find_all(class_='fs-14')
    print(rooms)


