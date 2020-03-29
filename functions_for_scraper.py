import json

def options_creator(house_dict)
    zipcode_dict = json.loads(open('Postcode_damsco.txt', 'r').read())

    options = {key: house_info for key, house_info in house_dict.items() 
                if house_info[1][:4] in zipcode_dict 
                and int(house_info[2][1:].replace(',-', '')) <= 1600
                and int(house_info[3][:-3]) >= 50 
                and int(house_info[4]) >= 2}

    return options

        
def zipcode_search(streetname):
    
    streetname= streetname.strip()
    streetname = streetname.replace(' ', '+')
    streetname += '+Amsterdam'
    
    # Google Geocoding API
    input = 'https://maps.googleapis.com/maps/api/geocode/json?address='+streetname+'&key=AIzaSyBAVfjRxqU9ynAFuq_DQ_JWRbSgI0Jy0gw'

    # Get input and create json
    r = requests.get(input)
    data = r.json()

    return data['results'][0]['address_components'][6]['long_name'][:4]

           