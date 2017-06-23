import csv
import matplotlib.pyplot as plt
from numpy.random import random
import plotly
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go
import math

plotly.tools.set_credentials_file(username='tylershyoon', api_key='o7KROcARRCiNcGLa1jm0')

geneM = {}
geneS = {}

with open("j2m_known_v4.csv", "rb") as csvfile:
    reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in reader:
        if row[0].split(',')[0] in ['ucsc', 'bamfile']:
            continue
        rowsplit = row[0].split(',')
        ucscID = rowsplit[0]
        name = rowsplit[1]
        UTR = rowsplit[4]
        Exons = rowsplit[-1]
        if float(Exons) != 0:
            #geneM.append([name, math.log(float(UTR)/float(Exons),2)])
            print "CHECK", name, float(UTR), float(Exons), float(UTR)/float(Exons)
            geneM[name] = float(UTR)/float(Exons)
            if geneM[name] > 10:
                geneM[name] = 10
        else:
            print "Exons->0: ", ucscID
            geneM[name] = 'NaN'

with open("j2m_unknown_v4.csv", "rb") as csvfile:
    reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row2 in reader:
        if row2[0].split(',')[0] in ['ucsc', 'bamfile']:
            continue
        rowsplit = row2[0].split(',')
        ucscID = rowsplit[0]
        name = rowsplit[1]
        UTR = rowsplit[4]
        Exons = rowsplit[-1]
        if float(Exons) != 0:
            #geneM.append([name, math.log(float(UTR)/float(Exons),2)])
            geneM[name] = float(UTR)/float(Exons)
            if geneM[name] > 10:
                geneM[name] = 10
        else:
            print "Exons->0: ", ucscID
            geneM[name] = 'NaN'

with open("j2s_known_v4.csv", "rb") as csvfile:
    reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row3 in reader:
        if row3[0].split(',')[0] in ['ucsc', 'bamfile']:
            continue
        rowsplit = row3[0].split(',')
        ucscID = rowsplit[0]
        name = rowsplit[1]
        UTR = rowsplit[4]
        Exons = rowsplit[-1]
        if float(Exons) != 0:
            if float(UTR) == 0 :
                #geneS.append([name, 0])
                geneS[name] = 0
            else:
                #geneS.append([name, math.log(float(UTR)/float(Exons),2)])\
                geneS[name] = float(UTR)/float(Exons)
                if geneS[name] > 10:
                    geneS[name] = 10
        else:
            print "Exons->0: ", ucscID
            geneS[name] = 'NaN'

with open("j2s_unknown_v4.csv", "rb") as csvfile:
    reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in reader:
        if row[0].split(',')[0] in ['ucsc', 'bamfile']:
            continue
        rowsplit = row[0].split(',')
        ucscID = rowsplit[0]
        name = rowsplit[1]
        UTR = rowsplit[4]
        Exons = rowsplit[-1]
        if float(Exons) != 0:
            #geneS.append([name, math.log(float(UTR)/float(Exons),2)])
            geneS[name] = float(UTR)/float(Exons)
            if geneS[name] > 10:
                geneS[name] = 10
        else:
            print "Exons->0: ", ucscID
            geneS[name] = 'NaN'

if len(geneM) != len(geneM):
    print "Something is wrong length of geneM geneS different !!"
else:
    '''yy = []
    zz = []
    for key in geneM:
        yy.append(key)
        print geneM[key]
        print geneS[key]
        zz.append([geneM[key], geneS[key]])
    print len(yy) == len(zz)
    trace = go.Heatmap(z=zz,
                       x=['M phase', 'S phase'],
                       y=yy)
    data = [trace]

    layout = go.Layout(
        autosize=False,
        height=3000,
        width=400,
        title='',
        xaxis=dict(
            title='Cell cycle phase',
            autotick=False,
            ticks='',
            nticks=30
        ),
        yaxis=dict(
            title='x/y',
            ticks='',
            nticks=300,
            )
    )
    fig = {'data':data, 'layout':layout}
    py.plot(fig, filename='heatmap')
    '''