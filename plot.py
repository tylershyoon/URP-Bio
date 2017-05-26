import csv
import matplotlib.pyplot as plt
from numpy.random import random
import plotly
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go
plotly.tools.set_credentials_file(username='tylershyoon', api_key='o5UvcHLyrWqjsTjvTNUL')
# Learn about API authentication here: https://plot.ly/python/getting-started
# Find your api_key here: https://plot.ly/settings/api
colors = ['b', 'c', 'y', 'm', 'r']
rows = [e for e in range(300)]
tc = []
with open("j2s_known.csv", "rb") as csvfile:
    reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    i = 0;
    for row in reader:
        if row[0].split(',')[0] in ['ucsc',  'bamfile']:
            continue
        UTR = row[0].split(',')[4]
        Exons = row[0].split(',')[-1]
        rows[i] = plt.scatter(UTR, Exons, marker='x', color=colors[4])
        i+=1
        tc.append(row[0].split(',')[0]+":"+row[0].split(',')[1])

with open("j2s_unknown.csv", "rb") as csvfile:
    reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in reader:
        if row[0].split(',')[0] in ['ucsc',  'bamfile']:
            continue
        UTR = row[0].split(',')[4]
        Exons = row[0].split(',')[-1]
        rows[i] = plt.scatter(UTR, Exons, marker='x', color=colors[3])
        i+=1
        tc.append(row[0].split(',')[0]+":"+row[0].split(',')[1])

text = iter(tc)
'''
colors = ['b', 'c', 'y', 'm', 'r']

lo = plt.scatter(random(10), random(10), marker='x', color=colors[0])
ll = plt.scatter(random(10), random(10), marker='o', color=colors[0])
l  = plt.scatter(random(10), random(10), marker='o', color=colors[1])
a  = plt.scatter(random(10), random(10), marker='o', color=colors[2])
h  = plt.scatter(random(10), random(10), marker='o', color=colors[3])
hh = plt.scatter(random(10), random(10), marker='o', color=colors[4])
ho = plt.scatter(random(10), random(10), marker='x', color=colors[4])

text = iter(['Low Outlier', 'LoLo', 'Lo', 'Average', 'Hi', 'HiHi', 'High Outlier'])
'''

mpl_fig = plt.gcf()
plotly_fig = tls.mpl_to_plotly( mpl_fig )

for dat in plotly_fig['data']:
    t = text.next()
    dat.update({'name': t, 'text':t})

plotly_fig['layout']['showlegend'] = True
py.plot(plotly_fig)