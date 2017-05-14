from neo4jDBConstruction import classes
import xlrd
from py2neo import Node, Relationship
from py2neo import Graph, Path
from py2neo.ogm import *
import pymysql
import tools
import file_retrieval
import ast
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
    tx = graph.begin()
    print "connected ! "
    return tx, graph

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


def neo_knownGene(tx, graph):
    r2 = open("Round2", "r")
    nodeslst = r2.readlines()

    for node in nodeslst:
        G = classes.knownGene()
        g = ast.literal_eval(node)

        G.ucscGene = g[0]; G.geneSymbol = g[1]; G.accession = g[2]; G.chrom = g[3]
        G.strand = g[4]; G.txStart = g[5]; G.cdsStart = g[6]; G.cdsEnd = g[7]; G.txEnd = g[8]
        G.exonNum = g[9]

        tx.merge(G)

        exonStarts =  ['starts: '] + [ long(e) for e in g[10].rstrip().split(" ") ]
        exonEnds = ['ends: '] + [ long(e) for e in g[11].rstrip().split(" ") ]

        # number of exons
        prev_exon = classes.region()
        for i in range(1, int(g[9])+1):
            exon = classes.region()
            exon.ucscGene = g[0]
            exon.indicator = 'exon' + str(i)
            exon.chrom = g[3]
            exon.start = exonStarts[i]
            exon.end = exonEnds[i]
            exon.length = exonEnds[i] - exonEnds[i]

            tx.merge(exon)
            # indicates 'exon1' stretched out from gene node to exon 1 node
            if i == 1:
                G.exon1.add(exon)
                tx.graph.push(G)
            else:
                prev_exon.EE.add(exon)
                tx.graph.push(G)
            prev_exon = exon

        #graph.push(G)


tx, graph = neo_connection()

neo_knownGene(tx, graph)