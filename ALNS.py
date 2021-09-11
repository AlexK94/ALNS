from copy import deepcopy
import sys
import random as rnd
import math
from math import exp
import time
import numpy as np









Tour_Capacity = 15
max_day = 6*60*60

class touren:

    def __init__(self):
        self.touren = []
        self.kosten = 0
        self.fehlende = []

    
    # next neighbour Startheuristik
    def next_neighbour(self, nachfrage, kostenmatrix, von_co, zu_co):               
        zu_beliefern = deepcopy(nachfrage)
        offene_tour = False
        tour = []
        while zu_beliefern.count(1) > 0:

        
            if offene_tour == False:
                offene_tour = True
                liste_kosten = [[von_co[index],index] for index, n in enumerate(zu_beliefern) if n == 1]
         
            else:
                liste_kosten = [[kostenmatrix[tour[(len(tour)-1)]][index],index] for index, n in enumerate(zu_beliefern) if n==1]
                
            liste_kosten.sort(key=lambda x: (x[0]))
    
            tour.append(liste_kosten[0][1])
            zu_beliefern[liste_kosten[0][1]] = 0
               
            if len(tour) == Tour_Capacity or zu_beliefern.count(1) == 0:
                offene_tour = False
                self.touren.append(deepcopy(tour))
                tour.clear()
            
        
        
        self.kosten = kalkuliere_kosten(self.touren, kostenmatrix, von_co, zu_co)

    #savings Startheuristik
    def savings(self, nachfrage, kostenmatrix, von_co, zu_co):

        savings = []
        zuordnung = [[],[]]
        for n in range(len(nachfrage)):
            for j in range(len(nachfrage)):
                if not n == j:
                    savings.append(zu_co[n] + von_co[j]- kostenmatrix[n,j] )
                    zuordnung[0].append(n)
                    zuordnung[1].append(j)

        savings = list(zip(savings,zuordnung[0],zuordnung[1]))

        savings.sort(key=lambda x: (x[0]), reverse= True)


        self.touren = []

        for n in range(len(nachfrage)):
            self.touren.append([n])

        for n in savings:
            stelle_i = []
            stelle_j = []
            gefunden = 0
            for i in range(len(self.touren)):
                for j in range(len(self.touren[i])):
                    if self.touren[i][j] == n[1]:
                        stelle_i.append(i)
                        stelle_i.append(j)
                        gefunden += 1
                    elif self.touren[i][j] == n[2]:
                        stelle_j.append(i)
                        stelle_j.append(j)
                        gefunden +=1
                    
                    if gefunden == 2:
                        break
                else: 
                    continue
                break
            
            length_j = len(self.touren[stelle_j[0]])
            length_i = len(self.touren[stelle_i[0]])
            
            if not stelle_i[0] == stelle_j[0]:
                if length_i + length_j <= Tour_Capacity:
                    if stelle_i[1] == length_i -1  and stelle_j[1] == 0:
                        self.touren[stelle_i[0]].extend(self.touren[stelle_j[0]])
                        del self.touren[stelle_j[0]]

                    
          
        
        
        

        self.kosten = kalkuliere_kosten(self.touren, kostenmatrix, von_co, zu_co)





    # alle Destroy Operatoren
    def destroy(self, nummer, untere, obere, gleiche_tour_parameter, kostenmatrix, von_co, zu_co, nr_custom, zufallsmesszahl):
        zu_entfernende = rnd.randint(untere,obere)
        
        if nummer == 0:             #Random Removal Kunden
            for n in range(zu_entfernende):
                i = rnd.randint(0, len(self.touren)-1)
                k = rnd.randint(0, len(self.touren[i])-1)
                self.fehlende.append(self.touren[i][k])
                self.touren[i].pop(k)
                if len(self.touren[i]) == 0:
                    del self.touren[i]

        if nummer == 1:             #Random Removal Touren
            entfernte = 0
            while zu_entfernende > entfernte:
                i = rnd.randint(0, len(self.touren)-1)
                for n in self.touren[i]:
                    self.fehlende.append(n)
                
                entfernte += len(self.touren[i]) 

                del self.touren[i] 
        
        if nummer == 2:             #Seed Kunde
            i = rnd.randint(0, len(self.touren)-1)
            k = rnd.randint(0, len(self.touren[i])-1)
            
                    
            seed = self.touren[i][k]
            kunden = []
            zuordnung = []
            for index, n in enumerate(self.touren):
                kunden += n
                zuordnung += [index] * len(n)


            distance = kostenmatrix[seed, kunden]
            kunden_sortiert = list(zip(distance, zuordnung, kunden))

            
            
            
            
            kunden_sortiert.sort(key=lambda x: (x[0]), reverse= True)


            zeilen = set()    
            for n in range(zu_entfernende):
                listenindex = int(math.ceil(rnd.random()**zufallsmesszahl*(len(kunden_sortiert)-1)))
                self.fehlende.append(kunden_sortiert[listenindex][2])
                zeile = kunden_sortiert[listenindex][1]
                self.touren[zeile].remove(kunden_sortiert[listenindex][2])
                zeilen.add(zeile)

                del kunden_sortiert[listenindex]
            
            self.touren = entferne_leere_Zeilen(self.touren, zeilen)

            

        if nummer == 3:             # Worst Removal
            kunden_sortiert =[]
            zuordnungen = [[],[],[],[]]
            einzeltouren = []
            erste_punkte = []
            letzte_punkte = []
            von =[]
            mitte= []
            zu = []
            for index, n in enumerate(self.touren):
                length = len(n)
                if length == 1:
                    einzeltouren += n
                    zuordnungen[0].append(index)

                else: 
                    erste_punkte.append(n[:2])
                    zuordnungen[1].append(index)
                    letzte_punkte.append(n[-2:])
                    zuordnungen[2].append( index)
                    if length > 2:
                        von += n[:-2]
                        mitte += n[1:-1]
                        zu += n[2:]
                        zuordnungen[3] += [index] * (length -2)

            if len(einzeltouren) > 0:
                einzeltouren = np.array(einzeltouren)  
                einzeltouren = list(zip(von_co[einzeltouren] + zu_co[einzeltouren], zuordnungen[0],einzeltouren ))

            erste_punkte = np.array(erste_punkte)
            spalte_1 = erste_punkte[:,0]
            spalte_2 = erste_punkte[:, 1]
            erste_punkte = list(zip(von_co[spalte_1] + kostenmatrix[spalte_1, spalte_2] - von_co[spalte_2],  zuordnungen[1], spalte_1))


            
            
            letzte_punkte = np.array(letzte_punkte)
            spalte_1 = letzte_punkte[:,0]
            spalte_2 = letzte_punkte[:,1]
            letzte_punkte = list(zip(zu_co[spalte_2] + kostenmatrix[spalte_1, spalte_2] - zu_co[spalte_1],  zuordnungen[2], spalte_2 ))

            von = np.array(von)
            mitte = np.array(mitte)
            zu = np.array(zu)

            rest = list(zip(kostenmatrix[von, mitte]+kostenmatrix[mitte, zu] - kostenmatrix[von,zu],  zuordnungen[3], mitte))

            kunden_sortiert = einzeltouren + erste_punkte+ letzte_punkte + rest

            kunden_sortiert.sort(key=lambda x: (x[0]), reverse=True)

           
            zeilen = set()    
            for n in range(zu_entfernende):
                listenindex = int(math.ceil(rnd.random()**zufallsmesszahl*(len(kunden_sortiert)-1)))
                self.fehlende.append(kunden_sortiert[listenindex][2])
                zeile = kunden_sortiert[listenindex][1]
                self.touren[zeile].remove(kunden_sortiert[listenindex][2])
                zeilen.add(zeile)

                del kunden_sortiert[listenindex]
            
            self.touren = entferne_leere_Zeilen(self.touren, zeilen)

        
        if nummer == 4:             # kürzeste Touren
            kunden_sortiert = []
            for n in range(len(self.touren)):
                kunden_sortiert.append([len(self.touren[n]), n])

            kunden_sortiert.sort(key=lambda x: (x[0]))

            entfernte = 0
            zeilen_ausgewählt = []
            while entfernte < zu_entfernende:

                listenindex = int(math.ceil(rnd.random()**zufallsmesszahl*(len(kunden_sortiert)-1)))
                zeile = kunden_sortiert[listenindex][1]
                self.fehlende += self.touren[zeile]
                
                
                zeilen_ausgewählt.append(zeile)
                entfernte += len(self.touren[zeile])
                
                
                del kunden_sortiert[listenindex]

            zeilen_ausgewählt.sort(reverse=True)
            for n in zeilen_ausgewählt:
                del self.touren[n]

            

        if nummer == 5:                 # gleiche Touren
            entfernte = 0
            while entfernte < zu_entfernende:
                i = rnd.randint(0, len(self.touren)-1)
                k = rnd.randint(0, len(self.touren[i])-1)

                seed = self.touren[i][k]
                kunden = []
                zuordnung = []
                for index, n in enumerate(self.touren):
                    kunden += n
                    zuordnung += [index] * len(n)


                distance = kostenmatrix[seed, kunden]
                kunden_sortiert = list(zip(distance, zuordnung, kunden))
            
                
                kunden_sortiert.sort(key=lambda x: (x[0]))

                zeilen = set()
                for n in range(1, gleiche_tour_parameter):
                    if not kunden_sortiert[0][1] == kunden_sortiert[n][1]:
                        for j in range(gleiche_tour_parameter):
                            self.touren[kunden_sortiert[j][1]].remove(kunden_sortiert[j][2])
                            entfernte +=1
                            zeilen.add(kunden_sortiert[j][1])
                            self.fehlende.append(kunden_sortiert[j][2])
                        break
                
                self.touren = entferne_leere_Zeilen(self.touren,zeilen)
               
                
                    





                    
            
    #alle repair Heuristiken

    def repair(self, nummer, stoerfaktor, kostenmatrix, von_co, zu_co, zufallsmesszahl):
                
        if nummer == 0:                 # Greedy Insertion
            while len(self.fehlende) >0:
                i = rnd.choice(self.fehlende)
                beste_stelle = bester_punkt(self.touren, i, kostenmatrix, von_co, zu_co)

                if len(beste_stelle)== 2:
                    self.touren[beste_stelle[0]].insert(beste_stelle[1],i)

                else:
                    self.touren.append([i])
                
                self.fehlende.remove(i)
            
              


        if nummer == 1:                 # Greedy Insertion mit Störfaktor
            while len(self.fehlende) >0:
                i = rnd.choice(self.fehlende)
                beste_stelle = bester_punkt_st(self.touren, i, stoerfaktor, kostenmatrix, von_co, zu_co)

                if len(beste_stelle)== 2:
                    self.touren[beste_stelle[0]].insert(beste_stelle[1], i)

                else:
                    self.touren.append([i])
                
                self.fehlende.remove(i)

        

        if nummer == 2:                 # K Regret Insertion
            fehlende_array = np.array(self.fehlende)
            zugewiesene = []
            for n in self.touren:
                zugewiesene += n
            next_point= np.amin(kostenmatrix[fehlende_array[:,None],zugewiesene], axis=1)

            next_point = list(zip(self.fehlende, next_point))
            next_point.sort(key=lambda x: (x[1]), reverse=True)

            while len(next_point) > 0:
                listenindex = int(math.ceil(rnd.random()**zufallsmesszahl*(len(next_point)-1)))
                beste_stelle = bester_punkt(self.touren, next_point[listenindex][0], kostenmatrix, von_co, zu_co)

                if len(beste_stelle)== 2:
                    self.touren[beste_stelle[0]].insert(beste_stelle[1], next_point[listenindex][0] )

                else:
                    self.touren.append([next_point[listenindex][0]])
                
                del next_point[listenindex]
            
            self.fehlende.clear()
            
       



        self.kosten = kalkuliere_kosten(self.touren, kostenmatrix, von_co,zu_co)



class Metaheuristiken:
    def __init__(self):
        self.beste_kosten = 0
        self.beste_tour = []
        self.bikes = 0
        self.D = []
        self.startkosten = 0
        self.score = [x[:] for x in [[1]*3]*6]
        self.beste =  np.zeros((6,3), dtype = int)
        self.verbesserte = np.zeros((6,3), dtype = int)
        self.akzeptiert = np.zeros((6,3), dtype = int)

    # ALNS 
    def ALNS(self, nachfrage, container, abbruchbedingung, untere, obere, koeffizient1, koeffizient2, koeffizient3, a, t_end_multiplikator, iterationen_anpassung, gewichtung, gleiche_tour_parameter, stoerfaktor, zufallsmesszahl):
        
        # Verkleinerung der Kostenmatrix

        demand_indices = np.nonzero(nachfrage)
        
        nr_custom = len(demand_indices[0])
        
        kostenmatrix = np.squeeze(distanzmatrix[demand_indices][:,demand_indices], axis=1)
        von_co = np.ravel(von_co_b[container,demand_indices])
        zu_co = np.ravel(zu_co_b[demand_indices, container])
        
        
        

        short_nachfrage = [1] * nr_custom
        #Startlösung initiieren
        aktuelle_loesung = touren()
        aktuelle_loesung.savings(short_nachfrage, kostenmatrix, von_co, zu_co)

        min_entfernt = int(untere * nr_custom)
        max_entfernt = int(obere * nr_custom)
        
        self.beste_kosten = aktuelle_loesung.kosten
        self.beste_tour = deepcopy(aktuelle_loesung.touren)
        print(self.beste_kosten)
        self.startkosten = self.beste_kosten
        t = self.beste_kosten * t_end_multiplikator
        
        benutzt= [x[:] for x in [[0]*3]*6]
        score_zwischenzeitlich = [x[:] for x in [[0]*3]*6]
        
        
        
        
        durchlaeufe_ohne_v = 0
        segment = 0
       
        #Bestimmung der Operatorenwahrscheinlichkeit
        gesamte_punkte = 0
        for n in range(len(self.score)):
            gesamte_punkte += sum(self.score[n])

        wahrscheinlichkeiten = []
        for n in range(len(self.score)):    
        
            wahrscheinlichkeiten.append ([i / gesamte_punkte for i in self.score[n]])

        

        while durchlaeufe_ohne_v < abbruchbedingung:
           
            veraenderte_l = deepcopy(aktuelle_loesung)
            durchlaeufe_ohne_v +=1
            verwendeter_operator = []

        

            #Auswahl der verwendeten Operatoren
            zu_zahl = rnd.random()

           

            for n in range(len(self.score)):
               
                for index, i in enumerate(wahrscheinlichkeiten[n]):
                    if zu_zahl <= i:
                        
                        veraenderte_l.destroy(n, min_entfernt, max_entfernt, gleiche_tour_parameter, kostenmatrix, von_co, zu_co, nr_custom,zufallsmesszahl)
                        
                        veraenderte_l.repair(index, stoerfaktor, kostenmatrix, von_co, zu_co, zufallsmesszahl)
                            
                        benutzt[n][index] += 1
                        verwendeter_operator.append(n)
                        verwendeter_operator.append(index) 
                        
                        break
                    else:
                        zu_zahl -=  i

                else:
                    continue

                break
                        
                         
            #Auswertung der neuen Lösung
            if veraenderte_l.kosten < aktuelle_loesung.kosten:
                
                

                
                aktuelle_loesung = deepcopy(veraenderte_l)

                if veraenderte_l.kosten < self.beste_kosten:
                    self.beste_kosten = veraenderte_l.kosten
                    
                    
                    self.beste_tour = deepcopy(veraenderte_l.touren)
                    score_zwischenzeitlich[verwendeter_operator[0]][verwendeter_operator[1]] += koeffizient1
                    self.beste[verwendeter_operator[0],verwendeter_operator[1]] += 1
                    durchlaeufe_ohne_v = 0

                else:
                    score_zwischenzeitlich[verwendeter_operator[0]][verwendeter_operator[1]] += koeffizient2
                    self.verbesserte[verwendeter_operator[0],verwendeter_operator[1]] += 1
                    
            
            else:
                er_kriterium = exp(-((veraenderte_l.kosten - aktuelle_loesung.kosten) / t) )

                if rnd.random()   <= er_kriterium:
                    
                    aktuelle_loesung = deepcopy(veraenderte_l)
                    
                    score_zwischenzeitlich[verwendeter_operator[0]][verwendeter_operator[1]] += koeffizient3
                    self.akzeptiert[verwendeter_operator[0],verwendeter_operator[1]] += 1

            segment += 1

            #Anpassung der Operatoren Gewichtung
            if segment == iterationen_anpassung:
                
                for n in range(len(self.score)):
                    for index, i in enumerate(self.score[n]):
                        if benutzt[n][index] != 0:
                            
                            self.score[n][index] = i * gewichtung + (1- gewichtung) *  score_zwischenzeitlich[n][index] / benutzt[n][index]
                
                segment = 0    
                
                benutzt= [x[:] for x in [[0]*3]*6]
                score_zwischenzeitlich = [x[:] for x in [[0]*3]*6] 

                gesamte_punkte = 0
                for n in range(len(self.score)):
                    gesamte_punkte += sum(self.score[n])

                wahrscheinlichkeiten = []
                for n in range(len(self.score)):    
                
                    wahrscheinlichkeiten.append ([i / gesamte_punkte for i in self.score[n]])       
          
           
                
          


            if time.time() - start >= 20*60:
                break 
            

            t *= a
        
        
        
        #Zuordnung der Touren zu den Cargo Bikes

        untere_grenze = math.ceil(self.beste_kosten / max_day)
        verbesserung = True
        while verbesserung == True:
            verbesserung = False
            bikes = [0] * untere_grenze
            offene_touren = []
            
            
            for n in range(len(self.beste_tour)):
                kosten = 0
                kosten += sum(kostenmatrix[self.beste_tour[n][k],self.beste_tour[n][k+1]] for k in range(len(self.beste_tour[n])-1))
                kosten += von_co[self.beste_tour[n][0]]
                kosten += zu_co[self.beste_tour[n][len(self.beste_tour[n])-1]]
                offene_touren.append(kosten)
            
            
            touren_kosten = deepcopy(offene_touren)
            offene_touren.sort( reverse=True)
            while len(offene_touren) > 0:
                bikes.sort()
                bikes[0] += offene_touren[0]
                
                
                if bikes[0]> max_day:
                    verbesserung = False
                    untere_grenze += 1
                    break

                offene_touren.pop()

        self.bikes = len(bikes)

        #2opt Verfahren für Minimierung der letzten Ankunftszeit
        multiplikator = [0.1, 0.25, 0.5, 0.75, 1]

        for n in multiplikator:
            bikes = round((len(touren_kosten) * n))
            solution = touren_2opt(touren_kosten, bikes)
            
            self.D.append([solution, bikes])
           
        self.D = np.array(self.D)
        

        self.score = np.array(self.score)
    #ALNS mit besten 5 Operatore Kombinationen
    def ALNS_best5(self, nachfrage, container, abbruchbedingung, untere, obere, koeffizient1, koeffizient2, koeffizient3, a, t_end_multiplikator, iterationen_anpassung, gewichtung, gleiche_tour_parameter, stoerfaktor, zufallsmesszahl):
        
        

        demand_indices = np.nonzero(nachfrage)
        
        nr_custom = len(demand_indices[0])
        
        kostenmatrix = np.squeeze(distanzmatrix[demand_indices][:,demand_indices], axis=1)
        von_co = np.ravel(von_co_b[container,demand_indices])
        zu_co = np.ravel(zu_co_b[demand_indices, container])
        
        
        

        short_nachfrage = [1] * nr_custom

        aktuelle_loesung = touren()
        aktuelle_loesung.savings(short_nachfrage, kostenmatrix, von_co, zu_co)

        min_entfernt = int(untere * nr_custom)
        max_entfernt = int(obere * nr_custom)
        
        self.beste_kosten = aktuelle_loesung.kosten
        self.beste_tour = deepcopy(aktuelle_loesung.touren)
        print(self.beste_kosten)
        self.startkosten = self.beste_kosten
        t = self.beste_kosten * t_end_multiplikator
        
        auswahl = [[0,0],[0,2],[2,0],[2,2],[3,2]]

        benutzt= [0 for i in range(5)]
        score_zwischenzeitlich = [0 for i in range(5)]
        score = [1 for i in range(5) ]
        
        
        
        
        durchlaeufe_ohne_v = 0
        segment = 0
       
        
        gesamte_punkte = sum(score)
        

        wahrscheinlichkeiten = [i / gesamte_punkte for i in score]
        

        

        while durchlaeufe_ohne_v < abbruchbedingung:
           
            veraenderte_l = deepcopy(aktuelle_loesung)
            durchlaeufe_ohne_v +=1
            verwendeter_operator = []

        

            
            zu_zahl = rnd.random()

           

            
               
            for index, i in enumerate(wahrscheinlichkeiten):
                if zu_zahl <= i:
                    
                    veraenderte_l.destroy(auswahl[index][0], min_entfernt, max_entfernt, gleiche_tour_parameter, kostenmatrix, von_co, zu_co, nr_custom,zufallsmesszahl)
                    
                    veraenderte_l.repair(auswahl[index][1], stoerfaktor, kostenmatrix, von_co, zu_co, zufallsmesszahl)
                        
                    benutzt[index] += 1
                    
                    verwendeter_operator.append(index) 
                    
                    break
                else:
                    zu_zahl -=  i

                
                        
                         

            if veraenderte_l.kosten < aktuelle_loesung.kosten:
                
                

                
                aktuelle_loesung = deepcopy(veraenderte_l)

                if veraenderte_l.kosten < self.beste_kosten:
                    self.beste_kosten = veraenderte_l.kosten
                    
                    
                    self.beste_tour = deepcopy(veraenderte_l.touren)
                    score_zwischenzeitlich[verwendeter_operator[0]] += koeffizient1
                    
                    durchlaeufe_ohne_v = 0

                else:
                    score_zwischenzeitlich[verwendeter_operator[0]] += koeffizient1
                    
                    
            
            else:
                er_kriterium = exp(-((veraenderte_l.kosten - aktuelle_loesung.kosten) / t) )

                if rnd.random()   <= er_kriterium:
                    
                    aktuelle_loesung = deepcopy(veraenderte_l)
                    
                    score_zwischenzeitlich[verwendeter_operator[0]] += koeffizient1
                    

            segment += 1

            if segment == iterationen_anpassung:
                
                
                for index, i in enumerate(score):
                    if benutzt[index] != 0:
                        
                        score[index] = i * gewichtung + (1- gewichtung) *  score_zwischenzeitlich[index] / benutzt[index]
                
                segment = 0    
                
                benutzt= [0 for n in range(5)]
                score_zwischenzeitlich = [0 for n in range(5)] 

                gesamte_punkte = sum(score)
        

                wahrscheinlichkeiten = [i / gesamte_punkte for i in score]
             
          
           
                
          


            if time.time() - start >= 20*60:
                break 
            

            t *= a
        
        
        


        untere_grenze = math.ceil(self.beste_kosten / max_day)
        verbesserung = True
        while verbesserung == True:
            verbesserung = False
            bikes = [0] * untere_grenze
            offene_touren = []
            
            
            for n in range(len(self.beste_tour)):
                kosten = 0
                kosten += sum(kostenmatrix[self.beste_tour[n][k],self.beste_tour[n][k+1]] for k in range(len(self.beste_tour[n])-1))
                kosten += von_co[self.beste_tour[n][0]]
                kosten += zu_co[self.beste_tour[n][len(self.beste_tour[n])-1]]
                offene_touren.append(kosten)
            
            
            touren_kosten = deepcopy(offene_touren)
            offene_touren.sort( reverse=True)
            while len(offene_touren) > 0:
                bikes.sort()
                bikes[0] += offene_touren[0]
                
                
                if bikes[0]> max_day:
                    verbesserung = False
                    untere_grenze += 1
                    break

                offene_touren.pop()

        self.bikes = len(bikes)


        multiplikator = [0.1, 0.25, 0.5, 0.75, 1]

        for n in multiplikator:
            bikes = round((len(touren_kosten) * n))
            solution = touren_2opt(touren_kosten, bikes)
            
            self.D.append([solution, bikes])
           
        self.D = np.array(self.D)
        

        self.score = np.array(self.score)
    
    #ALNS mit bester Operatorkombination

    def ALNS_best(self, nachfrage, container, abbruchbedingung, untere, obere,  a, t_end_multiplikator, gleiche_tour_parameter, stoerfaktor, zufallsmesszahl):
        
        

        demand_indices = np.nonzero(nachfrage)
        
        nr_custom = len(demand_indices[0])
        
        kostenmatrix = np.squeeze(distanzmatrix[demand_indices][:,demand_indices], axis=1)
        von_co = np.ravel(von_co_b[container,demand_indices])
        zu_co = np.ravel(zu_co_b[demand_indices, container])
        
        
        

        short_nachfrage = [1] * nr_custom

        aktuelle_loesung = touren()
        aktuelle_loesung.savings(short_nachfrage, kostenmatrix, von_co, zu_co)

        min_entfernt = int(untere * nr_custom)
        max_entfernt = int(obere * nr_custom)
        
        self.beste_kosten = aktuelle_loesung.kosten
        self.beste_tour = deepcopy(aktuelle_loesung.touren)
        print(self.beste_kosten)
        self.startkosten = self.beste_kosten
        t = self.beste_kosten * t_end_multiplikator
        
        
        
        
        
        
        durchlaeufe_ohne_v = 0
        
       
        
        

        

        while durchlaeufe_ohne_v < abbruchbedingung:
           
            veraenderte_l = deepcopy(aktuelle_loesung)
            durchlaeufe_ohne_v +=1
            

        

            
            

            veraenderte_l.destroy(2, min_entfernt, max_entfernt, gleiche_tour_parameter, kostenmatrix, von_co, zu_co, nr_custom,zufallsmesszahl)
                        
            veraenderte_l.repair(2, stoerfaktor, kostenmatrix, von_co, zu_co, zufallsmesszahl)
           

            
                        
                         

            if veraenderte_l.kosten < aktuelle_loesung.kosten:
                
                

                
                aktuelle_loesung = deepcopy(veraenderte_l)

                if veraenderte_l.kosten < self.beste_kosten:
                    self.beste_kosten = veraenderte_l.kosten
                    
                    
                    self.beste_tour = deepcopy(veraenderte_l.touren)
                    
                    durchlaeufe_ohne_v = 0

                
                    
            
            else:
                er_kriterium = exp(-((veraenderte_l.kosten - aktuelle_loesung.kosten) / t) )

                if rnd.random()   <= er_kriterium:
                    
                    aktuelle_loesung = deepcopy(veraenderte_l)
                    
           
                
          


            if time.time() - start >= 20*60:
                break 
            

            t *= a
        
        
        


        untere_grenze = math.ceil(self.beste_kosten / max_day)
        verbesserung = True
        while verbesserung == True:
            verbesserung = False
            bikes = [0] * untere_grenze
            offene_touren = []
            
            
            for n in range(len(self.beste_tour)):
                kosten = 0
                kosten += sum(kostenmatrix[self.beste_tour[n][k],self.beste_tour[n][k+1]] for k in range(len(self.beste_tour[n])-1))
                kosten += von_co[self.beste_tour[n][0]]
                kosten += zu_co[self.beste_tour[n][len(self.beste_tour[n])-1]]
                offene_touren.append(kosten)
            
            
            touren_kosten = deepcopy(offene_touren)
            offene_touren.sort( reverse=True)
            while len(offene_touren) > 0:
                bikes.sort()
                bikes[0] += offene_touren[0]
                
                
                if bikes[0]> max_day:
                    verbesserung = False
                    untere_grenze += 1
                    break

                offene_touren.pop()

        self.bikes = len(bikes)


        multiplikator = [0.1, 0.25, 0.5, 0.75, 1]

        for n in multiplikator:
            bikes = round((len(touren_kosten) * n))
            solution = touren_2opt(touren_kosten, bikes)
            
            self.D.append([solution, bikes])
           
        self.D = np.array(self.D)
        

        self.score = np.array(self.score)

    #ALNS ohne Simulated Annealing

    def ALNS_ohne_sa(self, nachfrage, container, abbruchbedingung, untere, obere, koeffizient1, koeffizient2, iterationen_anpassung, gewichtung, gleiche_tour_parameter, stoerfaktor, zufallsmesszahl):
        
        

        demand_indices = np.nonzero(nachfrage)
        
        nr_custom = len(demand_indices[0])
        
        kostenmatrix = np.squeeze(distanzmatrix[demand_indices][:,demand_indices], axis=1)
        von_co = np.ravel(von_co_b[container,demand_indices])
        zu_co = np.ravel(zu_co_b[demand_indices, container])
        
        
        

        short_nachfrage = [1] * nr_custom

        aktuelle_loesung = touren()
        aktuelle_loesung.savings(short_nachfrage, kostenmatrix, von_co, zu_co)

        min_entfernt = int(untere * nr_custom)
        max_entfernt = int(obere * nr_custom)
        
        self.beste_kosten = aktuelle_loesung.kosten
        self.beste_tour = deepcopy(aktuelle_loesung.touren)
        print(self.beste_kosten)
        self.startkosten = self.beste_kosten
        
        
        benutzt= [x[:] for x in [[0]*3]*6]
        score_zwischenzeitlich = [x[:] for x in [[0]*3]*6]
        
        
        
        
        durchlaeufe_ohne_v = 0
        segment = 0
       
        
        gesamte_punkte = 0
        for n in range(len(self.score)):
            gesamte_punkte += sum(self.score[n])

        wahrscheinlichkeiten = []
        for n in range(len(self.score)):    
        
            wahrscheinlichkeiten.append ([i / gesamte_punkte for i in self.score[n]])

        

        while durchlaeufe_ohne_v < abbruchbedingung:
           
            veraenderte_l = deepcopy(aktuelle_loesung)
            durchlaeufe_ohne_v +=1
            verwendeter_operator = []

        

            
            zu_zahl = rnd.random()

           

            for n in range(len(self.score)):
               
                for index, i in enumerate(wahrscheinlichkeiten[n]):
                    if zu_zahl <= i:
                        
                        veraenderte_l.destroy(n, min_entfernt, max_entfernt, gleiche_tour_parameter, kostenmatrix, von_co, zu_co, nr_custom,zufallsmesszahl)
                        
                        veraenderte_l.repair(index, stoerfaktor, kostenmatrix, von_co, zu_co, zufallsmesszahl)
                            
                        benutzt[n][index] += 1
                        verwendeter_operator.append(n)
                        verwendeter_operator.append(index) 
                        
                        break
                    else:
                        zu_zahl -=  i

                else:
                    continue

                break
                        
                         

            if veraenderte_l.kosten < aktuelle_loesung.kosten:
                
                

                
                aktuelle_loesung = deepcopy(veraenderte_l)

                if veraenderte_l.kosten < self.beste_kosten:
                    self.beste_kosten = veraenderte_l.kosten
                    
                    
                    self.beste_tour = deepcopy(veraenderte_l.touren)
                    score_zwischenzeitlich[verwendeter_operator[0]][verwendeter_operator[1]] += koeffizient1
                    
                    durchlaeufe_ohne_v = 0

                else:
                    score_zwischenzeitlich[verwendeter_operator[0]][verwendeter_operator[1]] += koeffizient2
                    
                    
            
            
            segment += 1

            if segment == iterationen_anpassung:
                
                for n in range(len(self.score)):
                    for index, i in enumerate(self.score[n]):
                        if benutzt[n][index] != 0:
                            
                            self.score[n][index] = i * gewichtung + (1- gewichtung) *  score_zwischenzeitlich[n][index] / benutzt[n][index]
                
                segment = 0    
                
                benutzt= [x[:] for x in [[0]*3]*6]
                score_zwischenzeitlich = [x[:] for x in [[0]*3]*6] 

                gesamte_punkte = 0
                for n in range(len(self.score)):
                    gesamte_punkte += sum(self.score[n])

                wahrscheinlichkeiten = []
                for n in range(len(self.score)):    
                
                    wahrscheinlichkeiten.append ([i / gesamte_punkte for i in self.score[n]])       
          
           
                
          


            if time.time() - start >= 20*60:
                break 
            

            
        
        
        
        

        untere_grenze = math.ceil(self.beste_kosten / max_day)
        verbesserung = True
        while verbesserung == True:
            verbesserung = False
            bikes = [0] * untere_grenze
            offene_touren = []
            
            
            for n in range(len(self.beste_tour)):
                kosten = 0
                kosten += sum(kostenmatrix[self.beste_tour[n][k],self.beste_tour[n][k+1]] for k in range(len(self.beste_tour[n])-1))
                kosten += von_co[self.beste_tour[n][0]]
                kosten += zu_co[self.beste_tour[n][len(self.beste_tour[n])-1]]
                offene_touren.append(kosten)
            
            
            touren_kosten = deepcopy(offene_touren)
            offene_touren.sort( reverse=True)
            while len(offene_touren) > 0:
                bikes.sort()
                bikes[0] += offene_touren[0]
                
                
                if bikes[0]> max_day:
                    verbesserung = False
                    untere_grenze += 1
                    break

                offene_touren.pop()

        self.bikes = len(bikes)


        multiplikator = [0.1, 0.25, 0.5, 0.75, 1]

        for n in multiplikator:
            bikes = round((len(touren_kosten) * n))
            solution = touren_2opt(touren_kosten, bikes)
            
            self.D.append([solution, bikes])
           
        self.D = np.array(self.D)
        

        self.score = np.array(self.score)       

#Kostenkalkulationsfunktion                 

def kalkuliere_kosten(touren, kostenmatrix, von_co, zu_co):
    
    touren.sort(key=len, reverse = True)
    NR_short_lists = 0
    for n in range(len(touren) -1, -1, -1):
        if not len(touren[n]) == 15:
            NR_short_lists += +1
        else: 
            break
                     
    kosten= 0
    if NR_short_lists > 0:
        touren_array = np.array(touren[:-NR_short_lists])
    else:
        touren_array =np.array(touren)
    
   
    if len(touren_array) >= 1:
          
        kosten += np.sum(kostenmatrix[touren_array[:,:-1],touren_array[:,1:]])
       
    
        kosten += np.sum(von_co[ touren_array[:,0]])
        kosten += np.sum(zu_co[touren_array[:,-1:]])
    
    
    for k in range(1,NR_short_lists+1):
        n = len(touren)- k
        length = len(touren[n])
        kosten += sum([kostenmatrix[touren[n][k],touren[n][k+1]] for k in range(length-1)])
        kosten += von_co[touren[n][0]]
        kosten += zu_co[touren[n][length-1]]

    return kosten

    
#bester Punkt zum Einfügen eines Kunden
def bester_punkt(touren, kunde, kostenmatrix, von_co, zu_co):
    guenstigste_kosten =sys.maxsize
    von = []
    zu = []
    letzte_werte = []
    erste_werte = []
    längen = []
    zuordnung = []
    touren.sort(key=len)
    for index,n in enumerate(touren):
        length =len(n)
        
        längen.append(length) 
        if length < 15:
            erste_werte.append(n[0]) 
            letzte_werte.append(n[-1]) 
            if length > 1:
                zuordnung.extend([index]*(length-1))
                von.extend(n[:-1]) 
                zu.extend(n[1:]) 
                
                
        else:
            break

    if len(erste_werte)>0:
        von = np.array(von)
        zu = np.array(zu)
        erste_werte = np.array(erste_werte)
        letzte_werte = np.array(letzte_werte)
        
        kosten_start = von_co[kunde]+ kostenmatrix[kunde,erste_werte] - von_co[erste_werte]
        if len(von) >0:    
            kosten_mitte = kostenmatrix[von,kunde] + kostenmatrix[kunde, zu] - kostenmatrix[von,zu]
            min_mitte = np.amin(kosten_mitte)
        else: 
            min_mitte = sys.maxsize
        kosten_ende = kostenmatrix[letzte_werte,kunde] + zu_co[kunde] - zu_co[letzte_werte]

        min_start = np.amin(kosten_start)
        
        min_ende = np.amin(kosten_ende)

        position = np.argmin(np.array([min_start, min_mitte, min_ende]))
        
        if position == 0:
            guenstigste_kosten =min_start
            beste_stelle = [np.argmin(kosten_start), 0]
        if position == 1:
            guenstigste_kosten = min_mitte
            
            stelle = np.argmin(kosten_mitte)
            zeile = zuordnung[stelle]
            zuordnung =np.array(zuordnung)
            
            beste_stelle = [zeile, np.count_nonzero(zuordnung[:(stelle+1)] == zeile)]

        if position == 2:
            guenstigste_kosten = min_ende
            stelle = np.argmin(kosten_ende)
            beste_stelle=[stelle, längen[stelle]]
        
    
    

    

    einfuegungs_kosten = von_co[kunde]+zu_co[kunde]

    if einfuegungs_kosten < guenstigste_kosten:
        
        beste_stelle = []

    return beste_stelle

#Bester Punkt zum Einfügen mit eine Zufallskomponente

def bester_punkt_st(touren, kunde, stoerfaktor, kostenmatrix, von_co, zu_co):
    guenstigste_kosten =sys.maxsize
    von = []
    zu = []
    letzte_werte = []
    erste_werte = []
    längen = []
    zuordnung = []
    touren.sort(key=len)
    for index,n in enumerate(touren):
        length =len(n)
        
        längen.append(length) 
        if length < 15:
            erste_werte.append(n[0]) 
            letzte_werte.append(n[-1]) 
            if length > 1:
                zuordnung.extend([index]*(length-1))
                von.extend(n[:-1]) 
                zu.extend(n[1:]) 
                
                
        else:
            break

    if len(erste_werte)>0:
        von = np.array(von)
        zu = np.array(zu)
        erste_werte = np.array(erste_werte)
        letzte_werte = np.array(letzte_werte)
        
        kosten_start = von_co[kunde]+ kostenmatrix[kunde,erste_werte] - von_co[erste_werte]
        kosten_start = kosten_start*np.random.uniform(1-stoerfaktor, 1+ stoerfaktor, len(kosten_start))
        if len(von) >0:    
            kosten_mitte = kostenmatrix[von,kunde] + kostenmatrix[kunde, zu] - kostenmatrix[von,zu]
            kosten_mitte = kosten_mitte*np.random.uniform(1-stoerfaktor, 1+ stoerfaktor, len(kosten_mitte))
            min_mitte = np.amin(kosten_mitte)
        else: 
            min_mitte = sys.maxsize
        kosten_ende = kostenmatrix[letzte_werte,kunde] + zu_co[kunde] - zu_co[letzte_werte]
        kosten_ende = kosten_ende*np.random.uniform(1-stoerfaktor, 1+ stoerfaktor, len(kosten_ende))

        min_start = np.amin(kosten_start)
        
        min_ende = np.amin(kosten_ende)

        position = np.argmin(np.array([min_start, min_mitte, min_ende]))
        
        if position == 0:
            guenstigste_kosten =min_start
            beste_stelle = [np.argmin(kosten_start), 0]
        if position == 1:
            guenstigste_kosten = min_mitte
            
            stelle = np.argmin(kosten_mitte)
            zeile = zuordnung[stelle]
            zuordnung =np.array(zuordnung)
            
            beste_stelle = [zeile, np.count_nonzero(zuordnung[:(stelle+1)] == zeile)]

        if position == 2:
            guenstigste_kosten = min_ende
            stelle = np.argmin(kosten_ende)
            beste_stelle=[stelle, längen[stelle]]
        
    
    

    

    einfuegungs_kosten = von_co[kunde]+zu_co[kunde]
    einfuegungs_kosten *= rnd.uniform(1-stoerfaktor, 1+ stoerfaktor)

    if einfuegungs_kosten < guenstigste_kosten:
        
        beste_stelle = []

    

    return beste_stelle
    
def entferne_leere_Zeilen(touren, zeilen):
    zeilen = list(zeilen)
    zeilen.sort(reverse= True)

    for n in zeilen:
        if len(touren[n]) == 0:
            del touren[n]
    
    return touren

#2 Opt Verfahren
def touren_2opt(touren_kosten, bikes):
    bike_kosten = [0] * bikes
    bikes_zuordnung = [[] for i in range(bikes)]
    touren_kosten.sort(reverse=True)

    for index_t, n in enumerate(touren_kosten):
        kleinste_kosten = min(bike_kosten)
        index = bike_kosten.index(kleinste_kosten)
        bike_kosten[index] += n
        bikes_zuordnung[index].append(index_t)

    solution = max(bike_kosten)

    verbesserung = True
    while verbesserung == True:
        verbesserung = False
        for n in range(len(bikes_zuordnung)):
            for index_j, j in enumerate(bikes_zuordnung[n]):
                for i in range(len(bikes_zuordnung)):
                    if not n == i:
                        for index_k, k in enumerate(bikes_zuordnung[i]):

                            dummy_bike_kosten = deepcopy(bike_kosten)
                            dummy_bike_kosten[n] += touren_kosten[k] - \
                                touren_kosten[j]
                            dummy_bike_kosten[i] += touren_kosten[j] - \
                                touren_kosten[k]

                            if max(dummy_bike_kosten) < solution:
                                solution = max(dummy_bike_kosten)
                                bike_kosten = deepcopy(dummy_bike_kosten)
                                bikes_zuordnung[n][index_j] = k
                                bikes_zuordnung[i][index_k] = j
                                verbesserung == True
                                break
                    else:
                        continue
                    break
                else:
                    continue
                break
            else:
                continue
            break
    return solution

#Einlesen der Datei und Speicherung aller Ergebnisse

datei_co = open("distanzmatrix_plaetze_from.txt","r")

von_co_b = []
for i in datei_co:
    kosten = [int(n) for n in i.split(";")]
    von_co_b.append(kosten)

von_co_b = np.array(von_co_b)



datei_co.close()



datei_zu = open("distanzmatrix_plaetze_to.txt","r")

zu_co_b =[]
for i in datei_zu:
    kosten = [int(n) for n in i.split(";")]
    zu_co_b.append(kosten)

zu_co_b = np.array(zu_co_b)


datei_zu.close()

datei_distanz = open("distanzmatrix.txt","r")

distanzmatrix = []

for i in datei_distanz:
    kosten = [int(n) for n in i.split(";")]
    distanzmatrix.append(kosten)


distanzmatrix = np.array(distanzmatrix)


datei_distanz.close()

startpunkte = ["corneliusplatz","marktplatz","fürstenplatz","martin-luther-platz","graf-adolf-platz"]
kilometer =[1,2,3,4,5]
anzahl_kunden = [100,200,300,400,500]

loesungen = open("ergebnisse.csv","w")

iterationen = 0

gesamtkosten_all = 0
dauer_all = 0
bikes_all = 0
startkosten_all = 0
D_all = np.zeros((5,2), dtype = int)
score_all =  np.zeros((6,3), dtype = int)
beste_all =  np.zeros((6,3), dtype = int)
verbesserte_all = np.zeros((6,3), dtype = int)
akzeptiert_all = np.zeros((6,3), dtype = int)

for i in kilometer:
    for k in anzahl_kunden:
        gesamtkosten = 0
        dauer = 0
        bikes = 0
        startkosten = 0
        D = np.zeros((5,2), dtype = int)
        score =  np.zeros((6,3), dtype = int)
        beste =  np.zeros((6,3), dtype = int)
        verbesserte = np.zeros((6,3), dtype = int)
        akzeptiert = np.zeros((6,3), dtype = int)
        
        for index, n in enumerate(startpunkte):

            nachfrage = []
            nachfrage_datei = open("nachfrage_"+str(n)+"_"+ str(k)+"_"+str(i)+".csv", "r")
            for m in nachfrage_datei:
                zeile = [int(n) for n in m.split(";")]
                nachfrage.append(zeile)
                
            
            nachfrage_datei.close()

            
            nachfrage = np.array(nachfrage)
            for l in nachfrage:
                start = time.time()
                alns = Metaheuristiken()
                alns.ALNS(l, index, 10000, 0.05, 0.05, 50, 30, 25, 0.85, 0.5, 300, 0.6, 4, 0.25,3)
                iterationen += 1
                ende = time.time()
                print(iterationen)
                print(ende-start)
                gesamtkosten += alns.beste_kosten
                dauer += ende-start
                bikes += alns.bikes
                D += alns.D
                score = score + alns.score
                beste += alns.beste
                verbesserte += alns.verbesserte
                akzeptiert += alns.akzeptiert
                startkosten += alns.startkosten

        gesamtkosten_all += gesamtkosten
        dauer_all += dauer
        bikes_all += bikes
        D_all += D
        score_all = score_all + score
        beste_all += beste
        verbesserte_all += verbesserte
        akzeptiert_all += akzeptiert
        startkosten_all += startkosten

        
        

        loesungen.write(str(i) +"; "+str(k)+"\n")
        loesungen.write("gesamtkosten = "+str(gesamtkosten/15))
        loesungen.write("\n startkosten = "+str(startkosten/15))
        loesungen.write("\n dauer = "+str(dauer/15))
        loesungen.write("\n bikes = "+str(bikes/15))
        loesungen.write("\n score = "+str(score/15))
        loesungen.write("\n beste = "+str(beste/15))
        loesungen.write("\n verbesserte = "+str(verbesserte/15))
        loesungen.write("\n  akzeptiert = "+str(akzeptiert/15))
        loesungen.write("\n D = "+str(D /15)+ "\n \n")
        

loesungen.write("gesamte Werte\n")
loesungen.write("gesamtkosten = "+str(gesamtkosten_all/225))
loesungen.write("\n startkosten = "+str(startkosten_all/225))
loesungen.write("\n dauer = "+str(dauer_all/225))
loesungen.write("\n bikes = "+str(bikes_all/225))
loesungen.write("\n score = "+str(score_all/225))
loesungen.write("\n beste = "+str(beste_all/225))
loesungen.write("\n verbesserte = "+str(verbesserte_all/225))
loesungen.write("\n  akzeptiert = "+str(akzeptiert_all/225))
loesungen.write("\n D = "+str(D_all /225)+ "\n \n")
        
    








        
                    



        



