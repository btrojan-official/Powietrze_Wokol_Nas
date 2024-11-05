from tkinter import *
import json
import requests

window = Tk()
window.title('Powietrze wokol nas - Trojan Bartosz')

def sortier(n):
    return n["city"]["name"]

airQualitySource = requests.get('https://api.gios.gov.pl/pjp-api/rest/station/findAll')
airQuality = json.loads(airQualitySource.content)
airQuality.sort(key=sortier)

def parseName(s):
    if(s=="Zielona Góra"):
        return "zielonagora"
    s = s[0].lower() + s[1::]
    s = s.replace("ń","n")
    s = s.replace("ó","o")
    s = s.replace("ł","l")
    s = s.replace("ź","z")
    s = s.replace(" ","")
    return s

def colorChange(info):
    if info == "Bardzo dobry":
        return "green"
    elif info == "Dobry":
        return "#72ed80"
    elif info == "Umiarkowany":
        return "#c4eb86"
    elif info == "Dostateczny":
        return "yellow"
    elif info == "Zły":
        return "orange"
    elif info == "Bardzo zły":
        return "red"
    else:
        return "black"


def airStationsUpdate():
    global options2
    global options3
    global dropdown2
    global clicked2
    global prev

    global no2
    global pm01
    global pm25

    if(prev == clicked.get() and len(options3)>0):
        if clicked.get() == "Gorzów":
            no2.config(text="")
            pm10.config(text="")
            pm25.config(text="")
        else:
            stacja = requests.get('https://api.gios.gov.pl/pjp-api/rest/aqindex/getIndex/' + str(options2[clicked2.get()]))
            station = json.loads(stacja.content)

            if(station['no2IndexLevel'] is not None):
                no2.config(text=station['no2IndexLevel']['indexLevelName'], fg=colorChange(station['no2IndexLevel']['indexLevelName']))
            else:
                no2.config(text="brak danych", fg="black")
            if (station['pm10IndexLevel'] is not None):
                pm10.config(text=station['pm10IndexLevel']['indexLevelName'], fg=colorChange(station['pm10IndexLevel']['indexLevelName']))
            else:
                pm10.config(text="brak danych", fg="black")
            if (station['pm25IndexLevel'] is not None):
                pm25.config(text=station['pm25IndexLevel']['indexLevelName'], fg=colorChange(station['pm25IndexLevel']['indexLevelName']))
            else:
                pm25.config(text="brak danych", fg="black")
    else:
        prev = clicked.get()

        options2.clear()
        options3.clear()

        if clicked.get()=="Gorzów":
            options3.append(" ")

        for el in airQuality:
            if(el["city"]["name"] == clicked.get()):
                options2[el["stationName"]] = el["id"]
                options3.append(el["stationName"])

        clicked2.set(options3[0])
        dropdown2 = OptionMenu(window, clicked2, *options3, command=choosen)
        dropdown2.grid(column=0, row=7, columnspan=2, padx=5)

        airStationsUpdate()

def choosen(e):
    cityName.config(text=parseName(clicked.get()))

    weatherSource = requests.get('https://danepubliczne.imgw.pl/api/data/synop/station/' + parseName(clicked.get()))
    weather = json.loads(weatherSource.content)

    temperature.config(text=weather["temperatura"])
    rain.config(text=weather["suma_opadu"])
    pressure.config(text=weather["cisnienie"])

    airStationsUpdate()

titleL = Label(text="Sprawdź pogodę w swojej okolicy!")
titleL.grid(column=0, row=0, columnspan=2, pady=5, padx=5)

clicked = StringVar()
clicked.set("Warszawa")
prev = "Warszawa"

options = ["Kraków", "Warszawa", "Poznań", "Lublin", "Wrocław", "Toruń", "Gorzów", "Zielona Góra", "Łódź", "Opole", "Rzeszów", "Białystok", "Gdańsk", "Katowice", "Kielce", "Olsztyn", "Szczecin"]
options.sort()

dropdown = OptionMenu(window, clicked, *options, command=choosen)
dropdown.grid(column=0, row=1, columnspan=2)

cityNameL = Label(text="Nazwa miasta: ")
cityNameL.grid(column=0, row=2, sticky=W, padx=5)
cityName = Label(text="")
cityName.grid(column=1, row=2)

temperatureL = Label(text="Temperatura: ")
temperatureL.grid(column=0, row=3, sticky=W, padx=5)
temperature = Label(text="")
temperature.grid(column=1, row=3)

rainL = Label(text="Wielkość opadów: ")
rainL.grid(column=0, row=4, sticky=W, padx=5)
rain = Label(text="")
rain.grid(column=1, row=4)

pressureL = Label(text="Ciśnienie: ")
pressureL.grid(column=0, row=5, sticky=W, padx=5)
pressure = Label(text="")
pressure.grid(column=1, row=5)

airL = Label(text="Jakość powietrza")
airL.grid(column=0, row=6, columnspan=2, pady=5, padx=5)

clicked2 = StringVar()

options2 = {}
options3 = []

no2L = Label(text="dwutlenek azotu: ")
no2L.grid(column=0, row=8, sticky=W, padx=5)
no2 = Label(text="")
no2.grid(column=1, row=8)

pm10L = Label(text="PM10: ")
pm10L.grid(column=0, row=9, sticky=W, padx=5)
pm10 = Label(text="")
pm10.grid(column=1, row=9)

pm25L = Label(text="PM25: ")
pm25L.grid(column=0, row=10, sticky=W, padx=5)
pm25 = Label(text="")
pm25.grid(column=1, row=10)

choosen("Siemka")

window.mainloop()
