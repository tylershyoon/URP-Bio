import xlrd
from py2neo import Node, Relationship
from py2neo import Graph, Path
from py2neo.ogm import *
import pymysql
import tools
#import file_retrieval
import ast
import copy
############################################################
# SUBTASK(1) Neo4j DB construction

# - Open emboj200894s3 excel file, retrieving element from
#   list of genes which has alu in its 3utr
# - Search ucsc mysql public database, retrieve information
#   about that gene
#   reference tables: kgXref, knownGene etc
# - Construct class and attributes, append it as a node to
#   neo4j database.
############################################################


def neo_connection():
    graph = Graph("http://neo4j:neo4jpwd@localhost:7474")
    print "connected ! "
    return graph

# For round 2,3
def neo_knownGene(graph, roundName):
    r2 = open(roundName, "r")
    nodeslst = r2.readlines()

    for node in nodeslst:
        g = ast.literal_eval(node)
        gene = Node("knownGene", ucscGene=g[0], geneSymbol=g[1], accession=g[2], chrom=g[3],
                 strand=g[4], txStart=g[5], cdsStart=g[6], cdsEnd=g[7], txEnd=g[8], exonNum=g[9], roundName=roundName)
        graph.create(gene)
        print "gene created"

        exonStarts =  ['starts: '] + [ long(e) for e in g[10].rstrip().split(" ") ]
        exonEnds = ['ends: '] + [ long(e) for e in g[11].rstrip().split(" ") ]

        exons = ['exons: '] + [ 0 for e in range(g[9])]
        if g[4] == '+':
            print "entered + "
            for i in range(1, int(g[9])+1):
                exons[i] = Node("exon"+str(i), ucscGene=g[0], indicator='exon'+str(i), chrom=g[3], start=exonStarts[i], end=exonEnds[i], length=exonEnds[i]-exonStarts[i])
                if i == 1:
                    E1 = Relationship(gene, "E1", exons[i])
                    graph.create(E1)
                else:
                    EE = Relationship(exons[i-1], "EE", exons[i])
                    graph.create(EE)
                if i == int(g[9]):
                    utr3 = Node("utr3", cdsEnd=g[7], txEnd=g[8])
                    graph.create(utr3)
                    EU = Relationship(exons[i], "EU", utr3)
                    graph.create(EU)
        else: # (-) strand
            print "entered - "
            for i in range(int(g[9]), 0, -1):
                exons[i] = Node("exon" + str(int(g[9])-i+1), ucscGene=g[0], indicator='exon' + str(int(g[9])-i+1), chrom=g[3],
                                start=exonStarts[i], end=exonEnds[i], length=exonEnds[i] - exonStarts[i])
                if i == int(g[9]):
                    E1 = Relationship(gene, "E1", exons[i])
                    graph.create(E1)
                else:
                    EE = Relationship(exons[i+1], "EE", exons[i])
                    graph.create(EE)
                if i == 1:
                    utr3 = Node("utr3", txStart=g[5], cdsStart=g[6])
                    graph.create(utr3)
                    EU = Relationship(exons[i], "EU", utr3)
                    graph.create(EU)

# For round 4
def neo_unknownGene(graph, roundName):
    r = open(roundName, "r")
    nodeslst = r.readlines()

    for node in nodeslst:
        g = ast.literal_eval(node)
        gene = Node("unknownGene", geneSymbol=g[0], chrom=g[1], strand=g[2], txStart=g[3], txEnd=g[4], exonNum=g[5], roundName=roundName)
        graph.create(gene)
        print "gene created"

        exonSizes = ['sizes: '] + [long(e) for e in g[6].rstrip().split(" ") ]
        exonStarts = ['starts: '] + [long(e) for e in g[7].rstrip().split(" ") ]

        exons = ['exons: '] + [ 0 for e in range(g[5])]
        if g[2] == '+':
            print "entered + "
            for i in range(1, int(g[5])+1):
                exons[i] = Node("exon"+str(i), geneSymbol=g[0], indicator='exon'+str(i), chrom=g[1], start=exonStarts[i], end=exonStarts[i]+exonSizes[i], length=exonSizes[i])
                if i == 1:
                    E1 = Relationship(gene, "E1", exons[i])
                    graph.create(E1)
                elif i != int(g[5]):
                    EE = Relationship(exons[i-1], "EE", exons[i])
                    graph.create(EE)
                else: # last exon
                    Elast = Relationship(exons[i-1], "EL", exons[i])
                    graph.create(Elast)
        else: # (-) strand
            print "entered - "
            for i in range(int(g[5]), 0, -1):
                exons[i] = Node("exon"+str(int(g[5])-i+1), geneSymbol=g[0], indicator='exon'+str(int(g[5])-i+1), chrom=g[1], start=exonStarts[i], end=exonStarts[i]+exonSizes[i], length=exonSizes[i])
                if i == int(g[5]):
                    E1 = Relationship(gene, "E1", exons[i])
                    graph.create(E1)
                elif i != 1:
                    EE = Relationship(exons[i+1], "EE", exons[i])
                    graph.create(EE)
                else:
                    Elast = Relationship(exons[i+1], "EL", exons[i])
                    graph.create(Elast)

if __name__ == "__main__":
    graph = neo_connection()
    #neo_knownGene(graph, 'Round2')
    #neo_knownGene(graph, 'Round3')
    #neo_unknownGene(graph, 'Round4_2')