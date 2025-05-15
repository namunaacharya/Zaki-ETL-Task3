import argparse
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
        else:
            while j >= 0 and planets[j].distance < current.distance:
                planets[j + 1] = planets[j]
                j -= 1
        planets[j + 1] = current
    return planets

def bubble_sort(planets,ascending=True):
    l = len(planets)
    for i in range(l):
        for j in range(0,l-i-1):
            if ascending:
                while planets[j].distance > planets[j + 1].distance:
                    planets[j], planets[j + 1] = planets[j + 1], planets[j]
            else:
                while planets[j].distance < planets[j + 1].distance:
                    planets[j], planets[j + 1] = planets[j + 1], planets[j]
    return planets

def main():
    parser = argparse.ArgumentParser(description="Sorting Process with diff. sorting algorithm")
    parser.add_argument('--sort', help='--sort apiA for ascending or --sort apiD for descending')
    parser.add_argument('--algorithm', help='--sort apiA for ascending or --sort apiD for descending')

    args = parser.parse_args()

    planets = pldata()

    options = ["apiA", "apiD"]
    if args.sort not in options:
        print("Invalid input.Use --sort apiA for ascending or --sort apiD for descending.")
        return

    if args.algorithm == "insertion":
        if args.sort[-1] == 'A':
            sorted_planets = insertion_sort(planets, ascending=True)
        elif args.sort[-1] == 'D':
            sorted_planets = insertion_sort(planets, ascending=False)
        else:
            print("invalid")

    elif args.algorithm == "bubble":
        if args.sort[-1] == 'A':
            sorted_planets = bubble_sort(planets, ascending=True)
        elif args.sort[-1] == 'D':
            sorted_planets = bubble_sort(planets, ascending=False)
        else:
            print("invalid")

    for planet in sorted_planets:
        print(planet)
    insertion_sort(planets)
    bubble_sort(planets)


if __name__=='__main__':
    main()
        

