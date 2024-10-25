from flask import Flask, request, render_template
from geopy.geocoders import Nominatim
from gmplot import gmplot
from geopy.distance import geodesic
import numpy as np

def nearest_neighbor_tsp(cities,dis):
    num_cities = len(cities)
    unvisited_cities = set(range(1, num_cities))
    current_city = 0
    tour = [current_city]

    while unvisited_cities:
        nearest_city = min(unvisited_cities, key=lambda city: dis[current_city][city])
        tour.append(nearest_city)
        unvisited_cities.remove(nearest_city)
        current_city = nearest_city

    tour.append(0)  # Return to the starting city
    return tour


app = Flask(__name__,template_folder='./templates',static_folder='./static')

@app.route('/')
def my_form():
    return render_template('myway.html')

@app.route('/',methods=['POST'])
def my_form_post():
    geolocator = Nominatim(user_agent="my_geocoder")
    text=request.form['u']
    name=text.split("<br>")
    Dis=[];Co=[]
    for i in range(len(name)):
        loc = geolocator.geocode(name[i])
        if loc:
            Co.append([])
            Co[i].append(loc.latitude)
            Co[i].append(loc.longitude)
        else:
            name.pop(i)
    for i in range(len(name)):
        Dis.append([])
        for j in range(len(name)):
            if(i<j):
                Dis[i].append(float(format(geodesic((Co[i][0],Co[i][1]), (Co[j][0],Co[j][1])).kilometers,".2f")))
            elif(i==j):
                Dis[i].append(0)
            else:
                Dis[i].append(Dis[j][i])

    Maploc=geolocator.geocode(name[0])
    gmap = gmplot.GoogleMapPlotter(Maploc.latitude,Maploc.longitude, 2,api="")

    path=nearest_neighbor_tsp(Co,Dis)
    for i in range(len(name)):
        gmap.marker(Co[i][0],Co[i][1], title=name[i])
    for i in range(len(path)-1):
        X=[Co[path[i]][0],Co[path[i+1]][0]]
        Y=[Co[path[i]][1],Co[path[i+1]][1]]
        gmap.plot(X,Y,"red")
    mapname=str(np.random.randint(1,1000))    
    gmap.draw("templates\map"+mapname+".html")
    return render_template("map"+mapname+".html")
if __name__ == '__main__':
      app.run();
