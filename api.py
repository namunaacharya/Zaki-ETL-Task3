import requests

class Planet:
    def __init__(self, name, distance):
        self.name = name
        self.distance = distance

    def __repr__(self):
        return f"Planet : {self.name}, Distance from Sun : {self.distance} million km"

def pldata():
    api_url = "https://api.le-systeme-solaire.net/rest/bodies/"
    response = requests.get(api_url)
    data = response.json()
    planet_data = []
    for b in data["bodies"]:
        if b.get("isPlanet"):
            name = b.get("englishName")
            semi_major_axis = b.get("semimajorAxis")
            if semi_major_axis is not None:
                distance = semi_major_axis / 1_000_000
                planet_data.append(Planet(name, distance))
    return planet_data

def insertion_sort(planets, ascending=True):
    for i in range(1, len(planets)):
        current = planets[i]
        j = i - 1
        if ascending:
            while j >= 0 and planets[j].distance > current.distance:
                planets[j + 1] = planets[j]
                j -= 1
        planets[j + 1] = current
    return planets

def as_sort(logger):
    planets = pldata()
    as_planets = insertion_sort(planets)
    for planet in as_planets:
        logger.info(planet)

def des_sort(logger):
    planets = pldata()
    des_planets = insertion_sort(planets)[::-1]  
    for planet in des_planets:
        logger.info(planet)