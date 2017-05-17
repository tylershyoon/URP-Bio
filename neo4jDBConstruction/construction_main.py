from neo4jDBConstruction import classes
import xlrd
from py2neo import Node, Relationship
from py2neo import Graph, Path
from py2neo.ogm import *
import pymysql
import tools
import file_retrieval
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

def neo_commit(tx):
    tx.commit()

# will not be used
def neo4j_initial_const():
    '''
        This function is for constructing neo4j nodes from records in excel file.
    '''
    tx, graph = neo_connection()
    graph.delete_all()
    ################################################
    embojwb = xlrd.open_workbook("emboj200894s3.xls")
    ws = embojwb.sheet_by_index(0)
    nrows = ws.nrows
    for row_num in range(1, nrows):
        exceltuple = classes.exceltuple
        exceltuple['properties']['ucscgene'] = ws.row_values(row_num)[1][1:]
        exceltuple['properties']['Name'] = ws.row_values(row_num)[2][1:]
        exceltuple['properties']['accession'] = ws.row_values(row_num)[3][1:]
        exceltuple['properties']['Alus'] = int(ws.row_values(row_num)[4])
        exceltuple['properties']['MinINV'] = int(ws.row_values(row_num)[5])
        exceltuple['properties']['Edited'] = ws.row_values(row_num)[6][1:]
        excelTupleNode = Node("")

# For round 2,3
def neo_knownGene(graph, roundName):
    r2 = open(roundName, "r")
    nodeslst = r2.readlines()

    for node in nodeslst:
        #G = classes.knownGene()
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
                    EE = Relationship(exons[i-1], "E->E", exons[i])
                    graph.create(EE)
                if i == int(g[9]):
                    utr3 = Node("utr3", cdsEnd=g[7], txEnd=g[8])
                    graph.create(utr3)
                    EU = Relationship(exons[i], "E->U", utr3)
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
                    EE = Relationship(exons[i+1], "E->E", exons[i])
                    graph.create(EE)
                if i == 1:
                    utr3 = Node("utr3", txStart=g[5], cdsStart=g[6])
                    graph.create(utr3)
                    EU = Relationship(exons[i], "E->U", utr3)
                    graph.create(EU)

# For round 4
def neo_unknownGene(graph, roundName):
    r = open(roundName, "r")
    nodeslst = r.readlines()

    for node in nodeslst:
        g = ast.literal_eval(node)
        gene = Node("unknownGene", )

graph = neo_connection()
neo_knownGene(graph, 'Round2')
neo_knownGene(graph, 'Round3')