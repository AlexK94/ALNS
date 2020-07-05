import geopy
import geopy.distance
import random as rnd


start = geopy.Point(51.226030, 6.778924) # Location-Daten vom Corneliusplatz


d = geopy.distance.geodesic(kilometers=1)



lat_norden = d.destination(point=start, bearing=0).latitude 
lon_osten = d.destination(point=start, bearing=90).longitude
lat_sueden = d.destination(point=start, bearing=180).latitude
lon_westen = d.destination(point=start, bearing=270).longitude

kundendatei = open("shops-düsseldorf.csv", "r")

kundendatei.readline()

kunden = []
for n in kundendatei:
    kunde = n.split(";")
    koordinaten= [float(n) for n in kunde[2].split("/")]
    kunde[2] = koordinaten[0]
    kunde.insert(3, koordinaten[1])
    del kunde[6:9]
    kunden.append(kunde)

kundendatei.close()  

zu_beliefern = [0]* len(kunden)

for n in range(len(kunden)):
    if lon_westen <= kunden[n][2] <= lon_osten and lat_sueden <= kunden[n][3] <= lat_norden:
        zu_beliefern[n] = 1



for index, n in enumerate (zu_beliefern):
    if n == 1:
        zu_beliefern[index] = rnd.randint(0,1)

n_datei = open("nachfrage.csv", "w")


n_datei.write(str(zu_beliefern[0]))
for n in range(1, len(zu_beliefern)):
    n_datei.write(";" + str(zu_beliefern[n]))

n_datei.close()