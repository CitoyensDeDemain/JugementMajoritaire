import pandas as pd
import random as rd
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton
import numpy as np

nbCand = 5
ind = None
nbElecteurs = 30
pas = 0.3
mouseCand = 1
epsilon = 0.03
colors = ["#A50026", "#EA5739","#FEFFBE", "#4BB05C", "#006837"]

fig, (ax, ax2) = plt.subplots(2,1, gridspec_kw={'height_ratios': [3, 1]})

def randomElecCand():
    global nbElecteurs
    xs = [rd.random() * 1.8 - 0.9 for x in range(nbElecteurs)]
    ys = [rd.random() * 1.8 - 0.9 for x in range(nbElecteurs)]

    xCand = [rd.random() * 1.8 - 0.9 for x in range(nbCand)]
    yCand = [rd.random() * 1.8 - 0.9 for x in range(nbCand)]

    return ((xs, ys),(xCand, yCand))

def getDistrib(xs, ys, xCand, yCand):
    distrib = pd.DataFrame(columns=["Cand"+str(x+1) for x in range(nbCand)])
    for iCand in range(nbCand):
        mentions = []
        for i in range(nbElecteurs):
            dist = np.sqrt((xs[i]-xCand[iCand])**2 + (ys[i]-yCand[iCand])**2)
            mentions += [max(5 - int(dist // pas),1)]
        distrib["Cand"+str(iCand+1)] = mentions

    for iCand in range(nbCand, len(xCand)):
        mentions = []
        for i in range(nbElecteurs):
            dist = np.sqrt((xs[i] - xCand[iCand]) ** 2 + (ys[i] - yCand[iCand]) ** 2)
            mentions += [max(5 - int(dist // pas), 1)]
        distrib["Mouse" + str(iCand - nbCand +1)] = mentions
    return distrib

def mentionsFromDistrib(distrib):
    mentionsCount = pd.DataFrame(columns=distrib.columns, index=[x for x in range(1,6)])

    for cand in distrib.columns:
        mentionsCount[cand] = distrib[cand].value_counts()
    mentionsCount = mentionsCount.loc[mentionsCount.index.sort_values(),].transpose().fillna(0)
    mentionsCount.reset_index(inplace=True)
    return mentionsCount

def get_ind_under_point(event):
    global epsilon
    global ind

    d = np.hypot(np.asarray(xs) - event.xdata, np.asarray(ys) - event.ydata)
    indseq, = np.nonzero(d == d.min())
    ind = indseq[0]
    if d[ind] >= epsilon:
        ind = None

def on_release(event):
    global ind
    global distVote

    if ind != None:
        ax2.clear()
        mentionsCount = mentionsFromDistrib(distVote)
        mentionsCount.plot(x='index', kind='barh', stacked=True,
                           colormap="RdYlGn", ax=ax2)
        ax2.legend(loc="center right")
        ax2.axvline(x=(len(distVote) - 1) // 2 + 0.5, color="black")
        plt.plot()

        ind = None

def on_click(event):
    global mouseCand
    global distVote
    global ind
    global xCand
    global yCand

    if(event.button is MouseButton.RIGHT):
        distVote = distVote[distVote.columns[:-1]]
        xCand = xCand[:-1]
        yCand = yCand[:-1]
        mouseCand -= 1

        mentionsCount = mentionsFromDistrib(distVote)
        mentionsCount.plot(x='index', kind='barh', stacked=True,
                           colormap="RdYlGn", ax=ax2)
        return None

    ax.clear()
    ax.set_xlim((-1, 1))
    ax.set_ylim((-1, 1))

    if(event.inaxes):
        get_ind_under_point(event)

        if(ind == None):
            cc = plt.Circle((event.xdata, event.ydata), 4, color=colors[0], linewidth=0)
            ax.add_artist(cc)
            for dist in range(4, 0, -1):
                cc = plt.Circle((event.xdata, event.ydata), pas * dist, color=colors[5 - dist], linewidth=0)
                ax.add_artist(cc)

            ## Mise à jour ax2
            ax2.clear()
            xNewCand, yNewCand = event.xdata, event.ydata
            xCand += [xNewCand]
            yCand += [yNewCand]
            mentions = []
            for i in range(nbElecteurs):
                dist = np.sqrt((xs[i] - xNewCand) ** 2 + (ys[i] - yNewCand) ** 2)
                mentions += [max(5 - int(dist // pas), 1)]
            distVote["Mouse " + str(mouseCand)] = mentions
            mouseCand += 1

            mentionsCount = mentionsFromDistrib(distVote)
            mentionsCount.plot(x='index', kind='barh', stacked=True,
                               colormap="RdYlGn", ax=ax2)
            ax2.axvline(x=(len(distVote) - 1) // 2 + 0.5, color="black")

    ax.plot(xs, ys, 'o', color="black")

    for i in range(len(xCand)):
        ax.plot(xCand[i], yCand[i], 'o')
    ax.set_xlim((-1, 1))
    ax.set_ylim((-1, 1))
    plt.legend(loc="center right")
    plt.show()

def on_mouse_move(event):
    """Callback for mouse movements."""
    global ind
    global distVote

    if ind is None:
        return
    if event.inaxes is None:
        return
    x, y = event.xdata, event.ydata
    xs[ind], ys[ind] = x, y

    ax.clear()
    distVote = getDistrib(xs, ys, xCand, yCand)
    ax.plot(xs, ys, 'o', color="black")
    for i in range(len(xCand)):
        ax.plot(xCand[i], yCand[i], 'o')
    ax.set_xlim((-1, 1))
    ax.set_ylim((-1, 1))
    plt.show()

(xs, ys), (xCand, yCand) = randomElecCand()
distVote = getDistrib(xs, ys, xCand, yCand)
mentionsCount = mentionsFromDistrib(distVote)

mentionsCount.plot(x='index', kind='barh', stacked=True,
                   colormap="RdYlGn", ax=ax2)

ax2.legend(loc="center right")
ax2.axvline(x=(len(distVote)-1) // 2+0.5, color="black")

ax.plot(xs,ys,'o', color="black")

for i in range(len(xCand)):
    ax.plot(xCand[i],yCand[i],'o')

plt.connect('button_press_event', on_click)
plt.connect('motion_notify_event', on_mouse_move)
plt.connect('button_release_event', on_release)

ax.set_xlim((-1, 1))
ax.set_ylim((-1, 1))
fig.set_figheight(7.5)
fig.set_figwidth(5.25)
plt.legend(loc="center right")
plt.show()