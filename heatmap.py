import csv
import matplotlib.pyplot as plt
from numpy.random import random
import plotly
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go
import math

plotly.tools.set_credentials_file(username='tylershyoon', api_key='o7KROcARRCiNcGLa1jm0')

geneM = []
geneS = []

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
            geneM.append([name, math.log(float(UTR)/float(Exons),2)])
        else:
            print "Exons->0: ", ucscID

with open("j2m_unknown_v4.csv", "rb") as csvfile:
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
            geneM.append([name, math.log(float(UTR)/float(Exons),2)])
        else:
            print "Exons->0: ", ucscID

with open("j2s_known_v4.csv", "rb") as csvfile:
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
            if float(UTR) == 0 :
                geneS.append([name, 0])
            else:
                geneS.append([name, math.log(float(UTR)/float(Exons),2)])
        else:
            print "Exons->0: ", ucscID

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
            geneS.append([name, math.log(float(UTR)/float(Exons),2)])
        else:
            print "Exons->0: ", ucscID

if len(geneM) != len(geneM):
    print "Something is wrong length of geneM geneS different !!"
else:
    yy = []
    zz = []
    for i in range(len(geneM)-1):
        yy.append(geneM[i][0])
        print zz
        print i
        zz.append([geneM[i][1], geneS[i][1]])

    trace = go.Heatmap(z=zz,
                       x=['M phase', 'S phase'],
                       y=yy)
    data = [trace]
    py.plot(data, filename='basic-heatmap')
