import pandas as pd
import random as rd
import matplotlib.pyplot as plt
import numpy as np

nbCandidats = 10
nbElecteurs = 100

distVote = pd.DataFrame(columns=["Cand"+str(x+1) for x in range(nbCandidats)])
for col in distVote.columns:
    distVote[col] = [rd.randint(1,7) for x in range(nbElecteurs)]

distribGroupes = pd.DataFrame(columns=["Cand"+str(x+1) for x in range(2)])
distribGroupes.loc[0,] = [7,6]
distribGroupes.loc[1,] = [3,1]
distribGroupes.loc[2,] = [3,4]
distribGroupes["Nb"] = [50,50,1]

def groupeToDistrib(distribGr):
    distribGroupes = distribGr.copy(deep=True)
    nbList = distribGroupes.pop("Nb")
    distrib = pd.DataFrame(columns=distribGroupes.columns)
    for i in nbList.index:
        nbElec = nbList[i]
        addDistrib = pd.DataFrame(columns=distribGroupes.columns,index=[x for x in range(nbElec)])
        addDistrib.loc[0:nbElec,] = distribGroupes.loc[i,].values
        distrib = pd.concat([distrib, addDistrib], ignore_index=True)
    return(distrib)

def JugementMajoritaire(distrib):
    candidats = distrib.columns
    convDistribMentions = pd.DataFrame(columns=distrib.columns)
    for cand in distrib.columns:
        convDistribMentions[cand] = distrib[cand].sort_values().values

    while (len(candidats) > 1):
        print(1)
        indexMed = (len(convDistribMentions)-1) // 2
        medians = convDistribMentions.loc[indexMed,]
        candidats = medians.loc[medians == max(medians),].index.values
        if len(candidats) == 1:
            # convDistribMentions = convDistribMentions.drop(indexMed)
            # convDistribMentions.reset_index(drop=True, inplace=True)
            print("Le gagnant par JM est " + candidats[0])
            break
        else:
            convDistribMentions = convDistribMentions[candidats].drop(indexMed)
            convDistribMentions.reset_index(drop=True, inplace=True)
            # print(medians)

    return(convDistribMentions)

def Uninominal1Tour(distrib):
    pref = pd.DataFrame(columns=["Pref"])

    for elec in distrib.T.columns:
        maxNote = max(distrib.T[elec])
        listPref = distrib.T.loc[distrib.T[elec] == maxNote,elec].index.values

        n = rd.randint(1,len(listPref))-1
        pref.loc[elec, "Pref"] = listPref[n]
    print(pref.value_counts())
    return(pref.value_counts())

def ChampionCondorcet(distrib):
    matricePref = pd.DataFrame(columns=distrib.columns)
    for i in range(len(distrib.columns)):
        for j in range(i+1,len(distrib.columns)):
            pref = pd.DataFrame(columns=["Pref"])
            Candi = distrib.columns[i]
            Candj = distrib.columns[j]

            for elec in distrib.index:
                if(distrib.loc[elec, Candi] > distrib.loc[elec, Candj]):
                    pref.loc[elec,"Pref"] = Candi
                elif(distrib.loc[elec, Candi] < distrib.loc[elec, Candj]):
                    pref.loc[elec, "Pref"] = Candj
                else:
                    pref.loc[elec, "Pref"] = [Candi,Candj][rd.randint(0,1)]

            matricePref.loc[Candi, Candj] = round(pref.value_counts().loc[Candi,]/len(distrib)*100)
            matricePref.loc[Candj, Candi] = round(pref.value_counts().loc[Candj,] / len(distrib) * 100)

    Champions = matricePref.loc[matricePref.min(axis=1) > 50,].index.values
    if(len(Champions) > 0):
        print("Champion de Condorcet : "+Champions[0])
    else :
        print("Pas de Champion")

    return(matricePref)

def plotDistrib(distrib):
    mentionsCount = pd.DataFrame(columns=distrib.columns, index=[x for x in range(1,8)])

    for cand in distrib.columns:
        mentionsCount[cand] = distrib[cand].value_counts()
    mentionsCount = mentionsCount.loc[mentionsCount.index.sort_values(),].transpose().fillna(0)
    mentionsCount.reset_index(inplace=True)

    plt.ion()
    mentionsCount.plot(x='index', kind='barh', stacked=True,
                       title='Mention majoritaire', figsize=(10, 1 * len(distrib.columns)),
                       colormap="RdYlGn", **{"width": 0.7})
    plt.legend(loc="center right")
    plt.axvline(x=(len(distrib)-1) // 2+0.5, color="black")
    plt.ylabel("Répartition", size = 20)
    plt.show()

    return(mentionsCount.set_index("index").T)

def plotMentions(mentions):

    mentionsCount = mentions.loc[mentions.index.sort_values(),].transpose().fillna(0)
    mentionsCount.reset_index(inplace=True)

    plt.ion()
    mentionsCount.plot(x='index', kind='barh', stacked=True,
                       title='Mention majoritaire', figsize=(10, 1 * len(mentions.columns)),
                       colormap="RdYlGn", **{"width": 0.7})
    plt.legend(loc="center right")
    plt.axvline(x=(mentions.sum()[0] - 1) // 2 + 0.5, color="black")
    plt.ylabel("Répartition", size = 20)
    plt.show()

    return (mentionsCount.set_index("index").T)

def plotDistribRef2(distrib, redBars = True):
    Cand1, Cand2 = distrib.columns
    newPlot = distrib[[Cand1, Cand2]].value_counts().reset_index().sort_values([Cand1, Cand2]).reset_index()
    newPlot[1] = 0
    countRef = distrib[Cand1].value_counts().sort_index().reset_index()
    countRef.columns = [Cand2, 1]
    newPlot = pd.concat([newPlot, countRef], ignore_index=True).fillna(0).astype(int)

    colors = ["#A50026", "#EA5739", "#FDBF6F","#FEFFBE", "#B7E075", "#4BB05C", "#006837"]
    plots = [newPlot.loc[i, [0, 1]] for i in range(len(newPlot))]

    plt.figure(figsize=(10, 2))
    plt.barh([Cand2, Cand1], plots[0], color=colors[newPlot.loc[0, Cand2] - 1])
    sum = np.array(plots[0])

    for i in range(1, len(newPlot)):
        plt.barh([Cand2, Cand1], plots[i], left=sum, color=colors[newPlot.loc[i, Cand2] - 1])
        sum += plots[i]

    sum = 0
    for i in range(len(countRef)):
        sum += countRef.loc[i,1]
        if(redBars):
            plt.axvline(x=sum, color="red")

    if(redBars):
        plt.axhline(y=-0.5, color="red")
        plt.axhline(y=1.5, color="red")
    plt.ylabel("Distribution", size=20)
    plt.show()

# JM / Condorcet / Uninominal
countMentionsDist = plotDistrib(distVote)

lastDistrib = JugementMajoritaire(distVote)
plotDistrib(lastDistrib)

uninominal = Uninominal1Tour(distVote)

condorcet = ChampionCondorcet(distVote)
print(condorcet)

## Création distributions spéciales

def creePrefCand2(mentions):
    Cand1, Cand2 = mentions.columns
    sum, distribErreur = 0, pd.DataFrame(columns=list(mentions.columns)+["Nb"])
    for gap in range(1,7):
        for j in range(1+gap,8):
            add = min(mentions.loc[j-gap,Cand1+(gap-1)*"*"],mentions.loc[j,Cand2+(gap-1)*"*"])
            sum += add
            mentions.loc[j-gap,Cand1+gap*"*"] = int(mentions.loc[j-gap,Cand1+(gap-1)*"*"] - add)
            mentions.loc[j,Cand2+gap*"*"] = int(mentions.loc[j,Cand2+(gap-1)*"*"] - add)
            if(add != 0):
                distribErreur = distribErreur.append({Cand1:j-gap, Cand2:j, "Nb": add}, ignore_index=True)
                print(add)
        mentions.loc[(7-gap+1):7,Cand1+gap*"*"] = mentions.loc[(7-gap+1):7,Cand1+(gap-1)*"*"]
        mentions.loc[1:gap, Cand2 + gap * "*"] = mentions.loc[1:gap, Cand2 + (gap-1) * "*"]

    mentionsFinales = mentions[mentions.columns[-2::]]
    mentionsFinales.columns = [Cand1,Cand2]
    print("Préférence de "+str(sum)+"% de l'électorat pour le candidat 2 : "+Cand2)
    return(distribErreur, mentionsFinales)

def creeEgalite(mentions):
    Cand1, Cand2 = mentions.columns
    sum, distribErreur = 0, pd.DataFrame(columns=list(mentions.columns) + ["Nb"])
    gap = 1
    for j in range(1,8):
        add = min(mentions.loc[j, Cand1], mentions.loc[j, Cand2])
        sum += add
        mentions.loc[j, Cand1 + gap * "*"] = int(mentions.loc[j, Cand1 + (gap - 1) * "*"] - add)
        mentions.loc[j, Cand2 + gap * "*"] = int(mentions.loc[j, Cand2 + (gap - 1) * "*"] - add)
        if (add != 0):
            distribErreur = distribErreur.append({Cand1: j, Cand2: j, "Nb": add}, ignore_index=True)
            print(add)
    mentionsFinales = mentions[mentions.columns[-2::]]
    mentionsFinales.columns = [Cand1, Cand2]
    print("Egalité sur " + str(sum) + "% de l'électorat.")
    return (distribErreur, mentionsFinales)

Cand1, Cand2 = "Cand7", "Cand9"
mentions = countMentionsDist[[Cand1,Cand2]]
distrib1, mentions1 = creePrefCand2(mentions)
distrib2, mentions2 = creeEgalite(mentions1)
distrib3, mentions3 = creePrefCand2(mentions2[[Cand2,Cand1]])

distribGroupesErreur = pd.concat([distrib1, distrib2, distrib3], ignore_index=True).astype(int)
distribErreur = groupeToDistrib(distribGroupesErreur)

mentionsNew = plotDistrib(distribErreur)
mentionsOld = plotDistrib(distVote[[Cand1,Cand2]])
jugementMajo = JugementMajoritaire(distribErreur)
plotDistrib(jugementMajo)

uninominalErreur = Uninominal1Tour(distribErreur)
uninominalOld = Uninominal1Tour(distVote[[Cand1,Cand2]])

plotDistribRef2(distribErreur[[Cand2,Cand1]])
plotDistribRef2(distVote[[Cand2,Cand1]])
plotDistribRef2(distribErreur[[Cand2,Cand1]], False)
plotDistribRef2(distVote[[Cand2,Cand1]], False)

# Cas particulier Laslier
distEtrange = groupeToDistrib(distribGroupes)
condorcetEtrange = ChampionCondorcet(distEtrange)
print(condorcetEtrange)
plotDistrib(distEtrange)


# Cas particulier : laprimairepopulaire.org 2022
mentionsGroupes = pd.DataFrame(columns=["Christiane Taubira", "Yannick Jadot", "Jean-Luc Mélenchon","Index"])
mentionsGroupes["Index"] = [1,2,3,4,5,6,7]
mentionsGroupes["Christiane Taubira"] = [0,13,8,12,18,49,0]
mentionsGroupes["Yannick Jadot"] = [0,19,15,21,23,21,0]
mentionsGroupes["Jean-Luc Mélenchon"] = [0,29,18,17,15,21,0]
mentionsGroupes = mentionsGroupes.set_index("Index")

plotMentions(mentionsGroupes)

Cand1, Cand2 = "Christiane Taubira", "Yannick Jadot"
mentionsPP = mentionsGroupes[[Cand1,Cand2]]
distribPP1, mentionsPP1 = creePrefCand2(mentionsPP)
distribPP2, mentionsPP2 = creeEgalite(mentionsPP1)
distribPP3, mentionsPP3 = creePrefCand2(mentionsPP2[[Cand2,Cand1]])

distribGroupesErreurPP = pd.concat([distribPP1, distribPP2, distribPP3], ignore_index=True).astype(int)
distribErreurPP = groupeToDistrib(distribGroupesErreurPP)

mentionsNewPP = plotDistrib(distribErreurPP)
uninominalErreurPP = Uninominal1Tour(distribErreurPP)
plotDistribRef2(distribErreurPP[[Cand2,Cand1]])