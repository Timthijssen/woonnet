import pandas as pd
import json

def option_selector(zipcodes, price, sq_meter, bedrooms):
    
    df_total_houses = pd.read_csv('huizen_alle.csv', index_col = 0)
    total_houses = df_total_houses.to_dict('index')

    options = {key: house_info for key, house_info in total_houses.items()
            if house_info['zipcode'][:4] in zipcodes
            and float((house_info['price'])) <= price
            and int(house_info['sq']) >= sq_meter
            and int(house_info['rooms']) >= bedrooms}
    
    return options




if __name__ == '__main__':    
    
    # set paramaters (Tim Tijmen - Amsterdam)
    zipcodes = json.loads(open('Postcode_damsco.txt', 'r').read())
    price = 1600.0
    sq_meter = 50
    bedrooms = 2
    file_name = 'opties_Amsterdam.csv'

    # set paramaters (Remco - Amsterdam)
    # zipcodes = json.loads(open('Remco_postcodes.txt', 'r').read())
    # price = 3500
    # sq_meter = 90
    # bedrooms = 4
    # file_name = 'opties_Remco_Amsterda.csv'
    
    # Creates options dateframe
    options = option_selector(zipcodes, price, sq_meter, bedrooms)
    df_options = pd.DataFrame.from_dict(data = options, orient='index', columns=['street', 'zipcode', 'price', 'sq', 'rooms', 'gestoffeerd', 'available', 'date added'])
    
    # Add new houses to dataframe and export
    df_options.to_csv(file_name)

