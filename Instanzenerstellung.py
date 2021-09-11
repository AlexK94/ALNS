import geopy
import geopy.distance
import random as rnd
from copy import deepcopy



container= [["corneliusplatz", 51.226030, 6.778924],["marktplatz", 51.226005, 6.771878],["fürstenplatz", 51.213452, 6.785326],["martin-luther-platz", 51.224009, 6.782064],["graf-adolf-platz", 51.219158, 6.777923]]
kilometer =[1,2,3]
anzahl_kunden = [100,200, 300, 400, 500]





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


for i in kilometer:

    for l in anzahl_kunden:
        for n in range(len(container)):
            start = geopy.Point(container[n][1], container[n][2])
            n_datei = open("nachfrage_"+str(container[n][0])+"_"+ str(l)+"_"+str(i)+"_test.csv", "w")

    
    


            d = geopy.distance.geodesic(kilometers=i)



            lat_norden = d.destination(point=start, bearing=0).latitude 
            lon_osten = d.destination(point=start, bearing=90).longitude
            lat_sueden = d.destination(point=start, bearing=180).latitude
            lon_westen = d.destination(point=start, bearing=270).longitude

            alle_kunden = [0]* len(kunden)

            for k in range(len(kunden)):
                if lon_westen <= kunden[k][2] <= lon_osten and lat_sueden <= kunden[k][3] <= lat_norden:
                    alle_kunden[k] = 1

            
            for m in range(3):
                anzahl = alle_kunden.count(1)
                print(anzahl)
                zu_beliefern = deepcopy(alle_kunden)
                while anzahl > l:
                    zu_entfernen = rnd.randint(0, anzahl-1)
                    zu_beliefern[[i for i, n in enumerate(zu_beliefern) if n == 1][zu_entfernen]] = 0
                    anzahl -= 1
                
                print(zu_beliefern.count(1))

                n_datei.write(str(zu_beliefern[0]))
                for n in range(1, len(zu_beliefern)):
                    n_datei.write(";" + str(zu_beliefern[n]))
                n_datei.write("\n")

            n_datei.close()

    