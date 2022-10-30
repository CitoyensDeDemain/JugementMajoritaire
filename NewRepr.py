import pandas as pd
import random as rd
import matplotlib.pyplot as plt
import numpy as np

nbCand = 5
pas = 0.3
colors = ["#A50026", "#EA5739","#FEFFBE", "#4BB05C", "#006837"]

fig, (ax, ax2) = plt.subplots(2,1, gridspec_kw={'height_ratios': [3, 1]})

xs = [rd.random() * 1.8 - 0.9 for x in range(30)]
ys = [rd.random() * 1.8 - 0.9 for x in range(30)]

xCand = [rd.random() * 1.8 - 0.9 for x in range(nbCand)]
yCand = [rd.random() * 1.8 - 0.9 for x in range(nbCand)]

distVote = pd.DataFrame(columns=["Cand"+str(x+1) for x in range(nbCand)])
for iCand in range(nbCand):
    mentions = []
    for i in range(30):
        dist = np.sqrt((xs[i]-xCand[iCand])**2 + (ys[i]-yCand[iCand])**2)
        mentions += [max(5 - int(dist // pas),1)]
    distVote["Cand"+str(iCand+1)] = mentions

mentionsCount = pd.DataFrame(columns=distVote.columns, index=[x for x in range(1,6)])

for cand in distVote.columns:
    mentionsCount[cand] = distVote[cand].value_counts()
mentionsCount = mentionsCount.loc[mentionsCount.index.sort_values(),].transpose().fillna(0)
mentionsCount.reset_index(inplace=True)

mentionsCount.plot(x='index', kind='barh', stacked=True,
                   colormap="RdYlGn", ax=ax2)

ax2.legend(loc="center right", )
ax2.axvline(x=(len(distVote)-1) // 2+0.5, color="black")

ax.plot(xs,ys,'o', color="black")

for i in range(nbCand):
    ax.plot(xCand[i],yCand[i],'o')

def on_click(event):
    if(not event.inaxes):
        return None

    ax.clear()
    for iCand in range(nbCand):

        if(abs(event.xdata - xCand[iCand]) < 0.05 and abs(event.ydata - yCand[iCand]) < 0.05):
            cc = plt.Circle((xCand[iCand], yCand[iCand]), 4, color=colors[0], linewidth=0)
            ax.add_artist(cc)
            for dist in range(4, 0, -1):
                cc = plt.Circle((xCand[iCand], yCand[iCand]), pas * dist, color=colors[5 - dist], linewidth=0)
                # cc2 = plt.Circle((xCand[iCand], yCand[iCand]), pas * (dist - 1), color='white', linewidth=0)
                ax.add_artist(cc)

    ax.plot(xs, ys, 'o', color="black")

    for i in range(nbCand):
        ax.plot(xCand[i], yCand[i], 'o')
    ax.set_xlim((-1, 1))
    ax.set_ylim((-1, 1))
    plt.show()

plt.connect('button_press_event', on_click)

ax.set_xlim((-1, 1))
ax.set_ylim((-1, 1))
fig.set_figheight(5)
fig.set_figwidth(3.5)
plt.margins(0.2)
plt.show()