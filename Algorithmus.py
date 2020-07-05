from copy import deepcopy
import sys
import random as rnd
import math
from math import exp

class touren:

    def __init__(self):
        self.touren = []
        self.kosten = 0
        self.fehlende = []

    

    def startloesung(self, nachfrage):
        zu_beliefern = deepcopy(nachfrage)
        offene_tour = False
        tour = []
        while zu_beliefern.count(1) > 0:

        
            if offene_tour == False:
                offene_tour = True
                liste_kosten = [von_co[0][index] for index, n in enumerate(zu_beliefern) if n == 1]
                guen_weg =  min(liste_kosten)

                iteration = -1
                for index, n in enumerate(zu_beliefern):
                    if n == 1:
                        iteration += 1
                        if iteration == liste_kosten.index(guen_weg):
                            zu_beliefern[index] = 0
                            tour.append(index)
                            break
            else:
                liste_kosten = [kostenmatrix[tour[(len(tour)-1)]][index] for index, n in enumerate(zu_beliefern) if n==1]
                guen_weg = min(liste_kosten)

                iteration = -1
                for index, n in enumerate(zu_beliefern):
                    if n==1:
                        iteration += 1
                        if iteration == liste_kosten.index(guen_weg):
                            zu_beliefern[index] = 0
                            tour.append(index)
                            if len(tour) == 10:
                                offene_tour = False
                                self.touren.append(deepcopy(tour))
                                tour.clear()
                            break
        self.touren.append(deepcopy(tour))
        self.kosten = kalkuliere_kosten(self.touren)


    def lokale_suche(self):
        andere_loesung = deepcopy(self.touren)

        uebrige_kunden = deepcopy(self.touren)
        while len(uebrige_kunden) > 0:
            i = rnd.randint(0, len(uebrige_kunden)-1)
            k = rnd.randint(0, len(uebrige_kunden[i])-1)

            for n in range(len(andere_loesung)):
                for m in range(len(andere_loesung[n])):
                    if andere_loesung[n][m] == uebrige_kunden[i][k]:
                        andere_loesung[n].pop(m) 
                        break



            guenstigste_kosten = sys.maxsize
            for n in range(len(self.touren)):
                if len(self.touren[n]) < 10:
                    for m in range(0,len(self.touren[n])):
                        if m == 0:
                            einfuegungs_kosten = von_co[0][uebrige_kunden[i][k]]+ kostenmatrix[uebrige_kunden[i][k]][self.touren[n][m]]
                            if einfuegungs_kosten < guenstigste_kosten:
                                guenstigste_kosten = einfuegungs_kosten
                                beste_stelle  = [n,m]


                        if m == (len(self.touren)-1):
                            einfuegungs_kosten = kostenmatrix[self.touren[n][m]][uebrige_kunden[i][k]] + zu_co[uebrige_kunden[i][k]][0]
                            if einfuegungs_kosten < guenstigste_kosten:
                                guenstigste_kosten = einfuegungs_kosten
                                beste_stelle = [n,m]

                        else:
                            einfuegungs_kosten = kostenmatrix[self.touren[n][m-1]][uebrige_kunden[i][k]]+ kostenmatrix[uebrige_kunden[i][k]][self.touren[n][m]]
                            if einfuegungs_kosten < guenstigste_kosten:
                                guenstigste_kosten = einfuegungs_kosten
                                beste_stelle = [n,m]
                        
                
            einfuegungs_kosten = von_co[0][uebrige_kunden[i][k]]+zu_co[uebrige_kunden[i][k]][0]
            
            if einfuegungs_kosten < guenstigste_kosten:
                andere_loesung.append(uebrige_kunden[i][k])
            
            else:
                andere_loesung[beste_stelle[0]].insert(beste_stelle[1], uebrige_kunden[i][k])

            andere_kosten = kalkuliere_kosten(andere_loesung)

            if andere_kosten < self.kosten:
                self.touren = deepcopy(andere_loesung)
                self.kosten = andere_kosten
                uebrige_kunden = deepcopy(andere_loesung)

            else:
                uebrige_kunden[i].pop(k)
                if len(uebrige_kunden[i]) == 0:
                    del uebrige_kunden[i]
                andere_loesung = deepcopy(self.touren)


    def destroy(self, nummer, untere, obere):
        zu_entfernende = rnd.randint(untere,obere)
        
        if nummer == 0:
            for n in range(zu_entfernende):
                i = rnd.randint(0, len(self.touren)-1)
                k = rnd.randint(0, len(self.touren[i])-1)
                self.fehlende.append(self.touren[i][k])
                self.touren[i].pop(k)
                if len(self.touren[i]) == 0:
                    del self.touren[i]

        if nummer == 2:
            entfernte = 0
            while zu_entfernende > entfernte:
                i = rnd.randint(0, len(self.touren)-1)
                for n in self.touren[i]:
                    self.fehlende.append(n)
                
                entfernte += len(self.touren[i]) 

                del self.touren[i] 
        
        if nummer == 1:
            i = rnd.randint(0, len(self.touren)-1)
            k = rnd.randint(0, len(self.touren[i])-1)

            kunden_sortiert = []
            zu_kunden = deepcopy(self.touren)

            kunden_sortiert.append(self.touren[i][k])
            zu_kunden[i].pop(k)
            if len(zu_kunden[i]) == 0:
                del zu_kunden[i]

            while len(zu_kunden) > 0:
                kuerzeste_laenge = sys.maxsize
                for n in range(len(zu_kunden)):
                    for j in range(len(zu_kunden[n])):
                        laenge = kostenmatrix[self.touren[i][k]][zu_kunden[n][j]]
                        if laenge < kuerzeste_laenge:
                            kuerzeste_laenge = laenge
                            naehester_kunde = [n, j]
                
                kunden_sortiert.append(zu_kunden[naehester_kunde[0]][naehester_kunde[1]])
                zu_kunden[naehester_kunde[0]].pop(naehester_kunde[1])

                if len(zu_kunden[naehester_kunde[0]]) == 0:
                    del zu_kunden[naehester_kunde[0]]

            for n in range(zu_entfernende):
                listenindex = int(math.ceil(rnd.random()**3*(len(kunden_sortiert)-1)))
                for n in range(len(self.touren)):
                    for index, i in enumerate (self.touren[n]):
                        if i == kunden_sortiert[listenindex]:
                            self.touren[n].pop(index)
                            kunden_sortiert.pop(listenindex)
                            self.fehlende.append(i)
                            if len(self.touren[n])== 0:
                                del self.touren[n]
                            break
                    else:
                        continue
                    break
                    
                

    def repair(self, nummer, stoerfaktor):
                
        if nummer == 0:
            while len(self.fehlende) >0:
                i = rnd.choice(self.fehlende)
                beste_stelle = bester_punkt(self.touren, i)

                if len(beste_stelle)== 2:
                    self.touren[beste_stelle[0]].insert(beste_stelle[1],i)

                else:
                    self.touren.append([i])
                
                self.fehlende.remove(i)
        
        if nummer == 1:
            while len(self.fehlende) >0:
                i = rnd.choice(self.fehlende)
                beste_stelle = bester_punkt_st(self.touren, i, stoerfaktor)

                if len(beste_stelle)== 2:
                    self.touren[beste_stelle[0]].insert(beste_stelle[1], i)

                else:
                    self.touren.append([i])
                
                self.fehlende.remove(i)

        self.kosten = kalkuliere_kosten(self.touren)



class Metaheuristiken:
    def __init__(self):
        self.beste_kosten = 0
        self.beste_tour = []

    
    def ALNS(self, nachfrage, untere, obere, koeffizient1, koeffizient2, koeffizient3, a):
        beste_loesung = touren()
        beste_loesung.startloesung(nachfrage)
        
        
        self.beste_kosten = beste_loesung.kosten
        print(self.beste_kosten)
        aktuelle_loesung = deepcopy(beste_loesung)
        
        t = self.beste_kosten * 1.5
        score = [x[:] for x in [[1]*2]*2]
        benutzt= [x[:] for x in [[0]*2]*2]
        score_zwischenzeitlich = [x[:] for x in [[0]*2]*2]
        
        vorgang = 0


        durchlaeufe_ohne_v = 0
        segment = 0

        while durchlaeufe_ohne_v < 20000:
            veraenderte_l = deepcopy(aktuelle_loesung)
            durchlaeufe_ohne_v +=1
            verwendeter_operator = []

            for n in range(len(score)):
                
                gesamt_score = sum(score[n])

                wahrscheinlichkeit = [i / gesamt_score for i in score[n]]

                zu_zahl = rnd.random()

                for index, i in enumerate(wahrscheinlichkeit):
                    if zu_zahl <= i:
                        if vorgang == 0:
                            veraenderte_l.destroy(index, untere, obere)
                            vorgang +=1
                        else: 
                            veraenderte_l.repair(index, 0.2)
                            vorgang = 0
                        benutzt[n][index] +=1
                        verwendeter_operator.append(index) 
                        break
                    else:
                        zu_zahl -=  i
                
            

            if veraenderte_l.kosten < aktuelle_loesung.kosten:
                
                

                
                aktuelle_loesung = deepcopy(veraenderte_l)

                if veraenderte_l.kosten < self.beste_kosten:
                    self.beste_kosten = veraenderte_l.kosten
                    print(self.beste_kosten)
                    beste_loesung = deepcopy(veraenderte_l)
                    score_zwischenzeitlich[0][verwendeter_operator[0]] += koeffizient1
                    score_zwischenzeitlich[1][verwendeter_operator[1]] += koeffizient1
                    durchlaeufe_ohne_v = 0

                else:
                    score_zwischenzeitlich[0][verwendeter_operator[0]] += koeffizient2
                    score_zwischenzeitlich[1][verwendeter_operator[1]] += koeffizient2
            
            else:
                er_kriterium = exp(-((veraenderte_l.kosten - aktuelle_loesung.kosten) / t) )

                if rnd.random()   <= er_kriterium:
                    
                    aktuelle_loesung = deepcopy(veraenderte_l)
                    
                    score_zwischenzeitlich[0][verwendeter_operator[0]] += koeffizient3
                    score_zwischenzeitlich[1][verwendeter_operator[1]] += koeffizient3

            segment += 1

            if segment == 100:
                
                for n in range(len(score)):
                    for index, i in enumerate(score[n]):
                        if benutzt[n][index] == 0:
                            benutzt[n][index] += 1
                        score[n][index] = i * 0.5 + 0.5 *  score_zwischenzeitlich[n][index] / benutzt[n][index]
                        print(score)
                
                benutzt= [x[:] for x in [[0]*2]*2]
                score_zwischenzeitlich = [x[:] for x in [[0]*2]*2]        

                segment = 0
            
            
            t *= a
        
        self.beste_tour = beste_loesung.touren


                 

def kalkuliere_kosten(touren):
    kosten = 0
    for n in range(len(touren)-1):
        kosten += sum(kostenmatrix[touren[n][k]][touren[n][k+1]] for k in range(len(touren[n])-1))
        kosten += von_co[0][touren[n][0]]
        kosten += zu_co[touren[n][len(touren[n])-1]][0]
    
    return kosten

def bester_punkt(touren, kunde):
    guenstigste_kosten = sys.maxsize
    for n in range(len(touren)):
        if len(touren[n]) < 10:
            for m in range(0,len(touren[n])):
                if m == 0:
                    einfuegungs_kosten = von_co[0][kunde]+ kostenmatrix[kunde][touren[n][m]]
                    if einfuegungs_kosten < guenstigste_kosten:
                        guenstigste_kosten = einfuegungs_kosten
                        beste_stelle  = [n,m]


                if m == (len(touren)-1):
                    einfuegungs_kosten = kostenmatrix[touren[n][m]][kunde] + zu_co[kunde][0]
                    if einfuegungs_kosten < guenstigste_kosten:
                        guenstigste_kosten = einfuegungs_kosten
                        beste_stelle = [n,m]

                else:
                    einfuegungs_kosten = kostenmatrix[touren[n][m-1]][kunde]+ kostenmatrix[kunde][touren[n][m]]
                    if einfuegungs_kosten < guenstigste_kosten:
                        guenstigste_kosten = einfuegungs_kosten
                        beste_stelle = [n,m]
                
        
    einfuegungs_kosten = von_co[0][kunde]+zu_co[kunde][0]
    
    if einfuegungs_kosten < guenstigste_kosten:
        beste_stelle = []

    return beste_stelle

def bester_punkt_st(touren, kunde, stoerfaktor):
    guenstigste_kosten = sys.maxsize
    for n in range(len(touren)):
        if len(touren[n]) < 10:
            for m in range(0,len(touren[n])):
                if m == 0:
                    einfuegungs_kosten = von_co[0][kunde]+ kostenmatrix[kunde][touren[n][m]]
                    einfuegungs_kosten *= rnd.uniform(1-stoerfaktor, 1+ stoerfaktor)
                    if einfuegungs_kosten < guenstigste_kosten:
                        guenstigste_kosten = einfuegungs_kosten
                        beste_stelle  = [n,m]


                if m == (len(touren)-1):
                    einfuegungs_kosten = kostenmatrix[touren[n][m]][kunde] + zu_co[kunde][0]
                    einfuegungs_kosten *= rnd.uniform(1-stoerfaktor, 1+ stoerfaktor)
                    if einfuegungs_kosten < guenstigste_kosten:
                        guenstigste_kosten = einfuegungs_kosten
                        beste_stelle = [n,m]

                else:
                    einfuegungs_kosten = kostenmatrix[touren[n][m-1]][kunde]+ kostenmatrix[kunde][touren[n][m]]
                    einfuegungs_kosten *= rnd.uniform(1-stoerfaktor, 1+ stoerfaktor)
                    if einfuegungs_kosten < guenstigste_kosten:
                        guenstigste_kosten = einfuegungs_kosten
                        beste_stelle = [n,m]
                
        
    einfuegungs_kosten = von_co[0][kunde]+zu_co[kunde][0]
    einfuegungs_kosten *= rnd.uniform(1-stoerfaktor, 1+ stoerfaktor)
    if einfuegungs_kosten < guenstigste_kosten:
        beste_stelle = []

    return beste_stelle
    


nachfrage_datei = open("nachfrage.csv", "r")
nachfrage = [int(n) for n in nachfrage_datei.readline().split(";")]
nachfrage_datei.close()

datei_co = open("distanzmatrix_plaetze_from.txt","r")

von_co = []
for i in datei_co:
    kosten = [int(n) for n in i.split(";")]
    von_co.append(kosten)

datei_co.close()

datei_zu = open("distanzmatrix_plaetze_to.txt","r")

zu_co =[]
for i in datei_zu:
    kosten = [int(n) for n in i.split(";")]
    zu_co.append(kosten)


datei_zu.close()

datei_distanz = open("distanzmatrix.txt","r")

kostenmatrix =[]

for i in datei_distanz:
    kosten = [int(n) for n in i.split(";")]
    kostenmatrix.append(kosten)


datei_distanz.close()




alns = Metaheuristiken()
alns.ALNS(nachfrage, 2, 15, 6, 3, 2, 0.999)

print(alns.beste_kosten)
    
      







        
                    



        



