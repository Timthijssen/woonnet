import json

zipcode_dict = json.loads(open('Postcode_damsco.txt', 'r').read())


options = {house[0]: house[1] for house in house_dict.items() 
               if house[1][1][:4] in zipcode_dict 
               and int(house[1][2][:-3]) >= 50 
               and int(house[1][3]) >= 2}


print(options)

        
        