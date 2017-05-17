import construction_main
from py2neo import Node, Relationship
from py2neo import Graph, Path
from pandas import DataFrame

def known_retrieval():
    graph = Graph("http://neo4j:neo4jpwd@localhost:7474")
    utrCypher = "MATCH (n:knownGene)-[:E1]-(e1)-[:EE*]-(last)-[:EU]-(utr) RETURN n.geneSymbol, utr.txStart, utr.cdsStart, utr.txEnd, utr.cdsEnd"
    testCypher = "MATCH (n:knownGene{geneSymbol:'ZYG11B'}) RETURN n"

    #results = graph.cypher.execute(utrCypher)
    lst = graph.data(testCypher)
    for elem in lst:
        print elem

def unknown_retrieval():
    pass

known_retrieval()