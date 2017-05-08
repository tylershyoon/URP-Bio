from neo4jDBConstruction import classes
import xlrd
from py2neo import Node, Relationship
from py2neo import Graph, Path
from py2neo.ogm import *

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
    return tx, graph

def neo_commit(tx):
    tx.commit()

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



neo4j_initial_const()

