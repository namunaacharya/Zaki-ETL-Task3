# For all heavenly bodies check if they are parameter with key 'isPlanet'
# If it is planet
# get the name of planet with key 'englishName'
# get the semi_major_axis (initially in km) using key 'semimajorAxis'
# get the distance using formula semi_major_axis/1000000 (convert km to million km)
# this distance is the distance from sun
# populate Parent class that will have two attributes: name, distance
# Using insertion sort, sort the planets by distance from the sun, display it in ascending or descending order depending on user input
# user input must be either apiA or apiD - api denotes that the api related code must be executed and the ending A or D denotes the sorting order

import requests

class API:
    def __init__(self, name, distance):
        self.name = name
        self.distance = distance  

    def __repr__(self):
        return f"planet : {self.name}, distance_from_sun : {self.distance} million km \n"

def pdata():
    api_url = "https://api.le-systeme-solaire.net/rest/bodies/"
    response = requests.get(api_url)
    data = response.json()
    planet_data = []
    for b in data["bodies"]:
        if b.get("isPlanet"):
            name = b.get('englishName')
            semi_major_axis = b.get('semimajorAxis')
            if semi_major_axis is not None:
                distance = semi_major_axis / 1_000_000  
                planet_data.append(API(name, distance))
    
    return planet_data
# df main():
#    planets = API.pdata()
#    for planet in planets:
#        print(planet)
# i __name__ == "__main__":
#    main()

planets = pdata()
for planet in planets:  
        print(planet)